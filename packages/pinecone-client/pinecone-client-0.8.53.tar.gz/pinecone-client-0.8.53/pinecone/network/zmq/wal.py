#
# Copyright (c) 2020-2021 Pinecone Systems Inc. All right reserved.
#
from pinecone.network.zmq.function_socket import FunctionSocket
from pinecone.utils.hash_ring import ConsistentHashRing

from .exceptions import InvalidOffsetException
from pinecone.protos import core_pb2
from pinecone.network.zmq.servlet import ZMQServlet
from pinecone.utils import open_or_create, get_hostname, wal, get_current_namespace, index_state, format_error_msg
from pinecone.utils.exceptions import RestartException
from pinecone.utils.constants import MAX_CLIENTS, ZMQ_LOG_PORT, MAX_MSGS_PENDING, KUBE_SYNC_TTL, \
    ZMQ_PORT_IN, IndexState, COMPACT_WAL_THRESHOLD
from pinecone.network.zmq.spec import ServletSpec, SocketType, Socket
from pinecone.network.zmq.socket_wrapper import SocketWrapper

from typing import Iterable, Tuple, List, Union
from loguru import logger

import concurrent.futures
from threading import Lock
import asyncio
import os
import functools
import mmap
import requests


class WALServlet(ZMQServlet):
    """
    ZMQServlet for distributed stateful functions to provide
    - client ordering guarantees
    - replay recovery from disk
    - leader-follower replication
    """

    def __init__(self, servlet_spec: ServletSpec, num_replicas: int, path: str, volume_request: int = 15):
        super().__init__(servlet_spec)
        self.replica = servlet_spec.replica
        self.num_replicas = num_replicas
        self.wal_size_limit = volume_request * (10 ** 9) * COMPACT_WAL_THRESHOLD  # translate to GB

        self.executor = concurrent.futures.ThreadPoolExecutor()

        self.log_in = self.init_socket(self.log_in_socket)
        self.log_out = self.init_socket(self.log_out_socket)

        self.in_buffer = asyncio.Queue()
        self.in_msgs = asyncio.Queue(maxsize=MAX_MSGS_PENDING)

        os.makedirs(path, exist_ok=True)

        self.log_path = os.path.join(path, 'log')
        self.tmp_log_path = os.path.join(path, 'tmp_log')  # for compaction
        self.log_file = open_or_create(self.log_path)
        self.log_lock = Lock()

        self.log_compaction_started = False

        self.last = core_pb2.Request()
        self.size = self.load_size()

        offset_path = os.path.join(path, 'offsets')
        self.offset_file = open_or_create(offset_path, truncate=wal.OFFSET_BYTES*self.num_replicas)
        self.offsets = mmap.mmap(self.offset_file.fileno(), 0)
        self.offset_locks = [Lock() for _ in range(0, self.num_replicas)]

        client_offsets_path = os.path.join(path, 'client_offsets')
        self.client_offsets_file = open_or_create(client_offsets_path, truncate=wal.OFFSET_BYTES*MAX_CLIENTS)

        self.client_offsets = mmap.mmap(self.client_offsets_file.fileno(), 0)
        self.client_offsets_locks = [Lock() for _ in range(0, MAX_CLIENTS)]

        self.hash_ring = ConsistentHashRing.from_file(servlet_spec.function_name, servlet_spec.native)
        self.rebalance_requested = False

        self._rebalance_sock_spec = Socket(False, SocketType.PUSH, ZMQ_PORT_IN, self.spec.function_name)
        self.rebalance_sock = FunctionSocket(self._rebalance_sock_spec, self.context, self.spec.native)

        self.index_ready = asyncio.Event()
        self.index_ready.set()

        self.compact_log_done = asyncio.Event()

    @property
    def log_in_socket(self):
        return Socket(True, SocketType.PULL, ZMQ_LOG_PORT, host=get_hostname())

    @property
    def log_out_socket(self):
        return Socket(False, SocketType.PUSH, host=self.spec.function_name, port=ZMQ_LOG_PORT)

    def load_size(self):
        size = 0
        for pos, entry in self.sync_replay_log(0):
            size += 1
            self.last = entry
        return size

    def cleanup(self):
        self.offset_file.close()
        self.log_file.close()
        super().cleanup()

    @property
    def leader(self):
        return self.replica == 0

    async def poll_log_socks(self):
        while True:
            msg = await self.recv_log_msg()
            await self.handle_log_msg(msg)

    def trigger_rebalance_shards(self):
        url = os.environ.get('CONTROLLER_URL')
        logger.info(f"{get_hostname()}: Triggering rebalance to {url}")

        project_name = get_current_namespace().replace(f"{self.spec.service_name}-", "")
        if len(project_name) == "":
            headers = {}
        else:
            # user label and user_name are placeholders, not used
            x_user_id = ".".join(['user_label', 'user_name', project_name])
            headers = {'x-user-id': x_user_id}
        resp = requests.patch(f'{url}/services/{self.spec.service_name}',
                              json={'function': {'name': self.spec.function_name, 'shards': self.hash_ring.size + 1}},
                              headers=headers).json()
        logger.info(resp)
        if not resp['success']:
            logger.error(f"Failed to trigger rebalance: {resp['msg']}. project: {project_name}. "
                         f"service: {self.spec.service_name}. function: {self.spec.function_name}. headers: {headers}")

    async def poll_sock(self, sock: SocketWrapper):
        loop = asyncio.get_event_loop()
        while True:
            msg = await self.recv_msg(sock)
            if self.hash_ring:
                msg.num_shards = self.hash_ring.size

            if self.use_wal(msg):
                await self.in_msgs.put(msg)
            else:
                await self.index_ready.wait()
                loop.create_task(self.handle_msg(msg))

    async def reload_hash_ring(self):
        loop = asyncio.get_event_loop()
        while True:
            new_hr = await loop.run_in_executor(self.executor, ConsistentHashRing.from_file, self.spec.function_name,
                                                self.spec.native)
            if self.hash_ring and new_hr.size != self.hash_ring.size:
                logger.info(f'Function size was: {self.hash_ring.size}. New size: {new_hr.size}. Rebalancing.')
                self.hash_ring = new_hr

                await self.start_compact_log(rebalance=True)
                self.rebalance_requested = False
            await asyncio.sleep(KUBE_SYNC_TTL)

    def start_reload_task(self) -> List[asyncio.Task]:
        loop = asyncio.get_event_loop()
        return [*super().start_reload_task(), loop.create_task(self.reload_hash_ring())]

    def start_polling(self) -> List[asyncio.Task]:
        loop = asyncio.get_event_loop()
        return [*(loop.create_task(self.poll_sock(sock.socket())) for sock in self.zmq_ins), loop.create_task(self.poll_log_socks())]

    def use_wal(self, msg: core_pb2.Request) -> bool:
        req_type = msg.WhichOneof('body')
        return req_type in ['index', 'delete']

    async def handle_msg_wal(self, msg: core_pb2.Request):
        msg_type = msg.WhichOneof('body')
        if self.hash_ring and msg_type == 'index':
            shard_msg = self.hash_ring.shard_msg(msg)
            for shard, msg in enumerate(shard_msg):
                if shard != self.spec.shard and len(msg.index.ids) > 0:
                    await self.forward_shard_msg(msg, shard)
            msg = shard_msg[self.spec.shard]

        new_offset = await self.put(msg)
        client_id = msg.client_id
        client_offset = msg.client_offset
        idx_state = await self.run_sync(index_state)
        if msg_type == 'index':
            if idx_state == IndexState.FULL:
                format_error_msg(msg, RuntimeError("Index full, cannot accept upserts"), self.pretty_name)
                await self.send_msg(msg)
                return
            elif idx_state == IndexState.PENDING and not self.rebalance_requested:
                await self.run_sync(self.trigger_rebalance_shards)
                self.rebalance_requested = True

        self.index_ready.clear()
        await self.wait_handlers_done()
        await self.handle_msg(msg)
        self.index_ready.set()
        await self.set_client_offset(client_id, client_offset + 1)
        await self.ack(new_offset)

    async def handle_log_msg(self, msg: 'core_pb2.LogEntry'):
        if not self.leader:
            try:
                if await self.put(msg.entry, offset=msg.offset):
                    self.index_ready.clear()
                    await self.wait_handlers_done()
                    await self.handle_msg(msg.entry)
                    self.index_ready.set()
            except InvalidOffsetException:
                logger.warning(f"Received invalid offset {msg.offset}")
                await self.send_log_msg(self.get_replay_request(), 0)
        else:
            await self.remote_ack(msg.offset, msg.ack.replica, msg.ack.replay)
            del msg

    async def consume_msgs(self):
        while True:
            msg = await self.in_msgs.get()
            if self.is_next(msg.client_id, msg.client_offset):
                await self.handle_msg_wal(msg)
                while True:
                    try:
                        await self.in_msgs.put(self.in_buffer.get_nowait())
                    except asyncio.QueueEmpty:
                        break
            else:
                # logger.error(f"Invalid client_offset {msg.client_offset}")
                if msg.client_offset >= self.get_client_offset(msg.client_id):
                    await self.in_buffer.put(msg)
                # elif msg.client_offset == self.get_client_offset(msg.client_id) - 1:
                #     await self.send_msg(msg)

    async def recv_log_msg(self):
        msg = await self.log_in.socket().recv()
        msg_pb = core_pb2.LogEntry()
        msg_pb.ParseFromString(msg)
        return msg_pb

    async def send_log_msg(self, msg: Union['core_pb2.LogEntry', bytes], replica: int):
        data = msg if type(msg) == bytes else msg.SerializeToString()
        await self.log_out.send_raw(data, shard=self.spec.shard, replica=replica)

    async def run_sync(self, func, *args, **kwargs):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self.executor, functools.partial(func, *args, **kwargs))

    def get_offset(self, replica: int):
        start = wal.OFFSET_BYTES * replica
        return int.from_bytes(self.offsets[start:start + wal.OFFSET_BYTES], wal.BYTEORDER)

    def offsets_list(self):
        return [self.get_offset(replica) for replica in range(0, self.num_replicas)]

    def write_offset(self, replica: int, offset: int):
        with self.offset_locks[replica]:
            self.offsets.seek(replica * wal.OFFSET_BYTES)
            self.offsets.write(offset.to_bytes(wal.OFFSET_BYTES, wal.BYTEORDER))
            self.offsets.flush()

    async def set_offset(self, replica: int, offset: int):
        await self.run_sync(self.write_offset, replica, offset)

    def get_client_offset(self, client_id: int):
        if client_id >= MAX_CLIENTS:
            return 0
        with self.client_offsets_locks[client_id]:
            start = client_id * wal.OFFSET_BYTES
            return int.from_bytes(self.client_offsets[start:start + wal.OFFSET_BYTES], wal.BYTEORDER)

    def is_next(self, client_id: int, client_offset: int):
        return True
        # if self.leader:
        #     if client_offset == 0:
        #         self.sync_set_client_offset(client_id, 0)  # should make this async
        #     return client_offset == self.get_client_offset(client_id)
        # else:
        #     return True

    def sync_set_client_offset(self, client_id: int, client_offset: int):
        if client_id >= MAX_CLIENTS:
            return
        with self.client_offsets_locks[client_id]:
            start = client_id * wal.OFFSET_BYTES
            self.client_offsets[start:start + wal.OFFSET_BYTES] = client_offset.to_bytes(wal.OFFSET_BYTES, wal.BYTEORDER)
            self.client_offsets.flush()

    async def set_client_offset(self, client_id: int, client_offset: int):
        if self.get_client_offset(client_id) > client_offset:
            return
        await self.run_sync(self.sync_set_client_offset, client_id, client_offset)

    def sync_put(self, entry: core_pb2.Request, offset: int):
        if (not offset) or (self.size + 1) == offset:
            with self.log_lock:
                wal.write_log_entry(self.log_file, entry)
                self.size += 1
                # we need to copy the message, because it might get changed later on
                self.last.CopyFrom(entry)
                logfile_size = self.log_file.tell()
            return logfile_size, self.size

        elif offset <= self.size:
            return self.log_file.tell(), None
        else:
            raise InvalidOffsetException

    async def put(self, item: core_pb2.Request, offset: int = None):
        if not self.leader and offset is None:
            raise RuntimeError(f"{get_hostname()} Attempted to write directly to replica {self.replica} instead of leader")
        logfile_size, offset = await self.run_sync(self.sync_put, item, offset)
        if logfile_size > self.wal_size_limit and not self.log_compaction_started:
            loop = asyncio.get_event_loop()
            logger.info(f'Starting WAL compaction. Log size: {logfile_size}')
            loop.create_task(self.start_compact_log())
        return offset

    def sync_replay_log(self, offset: int, end_offset: int = None) -> Iterable[Tuple[int, core_pb2.Request]]:
        """
        Replay log from offset 0 (inclusive) to end_offset (exclusive)
        :param offset:
        :param end_offset:
        :return:
        """
        with self.log_lock:
            self.log_file.seek(0)
            pos = 0
            while True:
                entry, msg_size = wal.read_entry(self.log_file)

                if msg_size == 0 or (end_offset and pos >= end_offset):
                    break
                if pos >= offset:
                    yield pos, entry
                pos += 1

    async def forward_shard_msg(self, msg: core_pb2.Request, shard: int):
        msg.client_offset = 0
        await self.rebalance_sock.send_msg(self.rebalance_sock.socket(shard, replica=0), msg)

    def handle_replay_request(self, loop: asyncio.AbstractEventLoop, replica: int, offset: int, end_offset: int = None):
        logger.info(f"Replaying log from offset {offset} to replica {replica}")
        for pos, entry in self.sync_replay_log(offset, end_offset=end_offset):
            asyncio.run_coroutine_threadsafe(self.send_log_msg(core_pb2.LogEntry(entry=entry,
                                                                                 offset=pos), replica), loop)

    def get_leader_log_backlog(self, replica: int) -> Iterable[core_pb2.LogEntry]:
        return [core_pb2.LogEntry(entry=entry, offset=offset)
                for offset, entry in self.sync_replay_log(self.get_offset(replica))]

    def sync_ack(self, offset: int):
        self.write_offset(self.replica, offset)

    async def ack(self, offset: int):
        prev_offset = self.get_offset(self.replica)
        if prev_offset > offset:
            logger.warning('Acked offset less than current offset')
        # elif prev_offset + 1 > offset:
        #     logger.warning('Acked by more than one offset')

        await self.set_offset(self.replica, offset)
        if self.leader:
            msg = core_pb2.LogEntry(entry=self.last, offset=offset)
            serialized_msg = msg.SerializeToString()
            for r in range(1, self.num_replicas):
                await self.send_log_msg(serialized_msg, r)

        else:
            ack = core_pb2.Ack(replica=self.replica)
            await self.send_log_msg(core_pb2.LogEntry(offset=offset, ack=ack), 0)

    async def remote_ack(self, start_offset: int, replica: int, replay=False):
        if replay:
            leader_offset = self.get_offset(self.replica)
            event_loop = asyncio.get_event_loop()
            await self.run_sync(self.handle_replay_request, event_loop, replica, start_offset, end_offset=leader_offset)

    def get_replay_request(self, override_offset=None):
        ack = core_pb2.Ack(replica=self.replica, replay=True)
        offset = override_offset or self.get_offset(self.replica)
        logger.info(f"Sending replay request for offset {offset}")
        return core_pb2.LogEntry(offset=offset, ack=ack)

    def load_sync(self, handler):
        logger.info(f'Recovering from local WAL: offset: {self.get_offset(self.replica)}')
        for offset, entry in self.sync_replay_log(self.get_offset(self.replica)):
            try:
                handler(entry)
            except Exception as e:  # ignore messages that fail
                logger.info(f'Error handling msg while recovering from WAL. offset: {offset} error: {e}')
            self.sync_ack(offset)

    def swap_log_files(self, end_file_offset: int):
        tmp_log_file = open(self.tmp_log_path, "r+b")

        with self.log_lock:
            self.log_file.seek(end_file_offset)
            while True:
                entry, msg_size = wal.read_entry(self.log_file)
                if msg_size == 0:
                    break
                wal.write_log_entry(tmp_log_file, entry)
            tmp_log_file.close()
            self.log_file.close()
            os.remove(self.log_path)
            os.rename(self.tmp_log_path, self.log_path)
            self.log_file = open(self.log_path, "r+b")

    async def start_compact_log(self, rebalance=False):
        while self.log_compaction_started:
            logger.info('Waiting for log compaction to be done to start again...')
            await self.compact_log_done.wait()
            self.compact_log_done.clear()

        with self.log_lock:
            self.log_compaction_started = True
            end_file_offset = self.log_file.tell()
            self.log_file.flush()
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(concurrent.futures.ProcessPoolExecutor(), wal.compact_log,
                                   self.log_path, self.tmp_log_path, end_file_offset, self.hash_ring, self.spec.shard,
                                   self._rebalance_sock_spec, self.spec.native)

        logger.info("Starting swap log files...")
        await self.run_sync(self.swap_log_files, end_file_offset)
        logger.info("Finishined swapping log files.")
        self.log_compaction_started = False
        self.compact_log_done.set()
        if rebalance:
            raise RestartException

    @property
    def all_socks(self):
        return [*super().all_socks, self.log_in, self.log_out]
