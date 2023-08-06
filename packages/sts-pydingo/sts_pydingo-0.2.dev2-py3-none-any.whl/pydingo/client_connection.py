import asyncio
import collections
import json
import threading
import urllib
import io

import PIL.Image

import tornado
import tornado.websocket

from .rpc_session import RPCSession

class RPCCallback(object):
    def __init__(self, object_type = None):
        self.ev = threading.Event()
        self.object_type = object_type

    def __call__(self, value):
        obj, bufs = value

        self.obj = obj
        if (self.object_type is not None):
            self.obj = self.object_type(self.obj)

        self.bufs = bufs

        self.ev.set()

    def wait(self):
        self.ev.wait()

class ClientConnection(object):
    def __init__(self, loop = None):
        if (loop is None):
            loop = asyncio.new_event_loop()

        self.loop = loop

        self.callbacks = {}

        self.next_id = 0

        self.rpc_session = RPCSession()
        self.vid_session = None


        th = threading.Thread(target = self.loop.run_forever)
        th.start()

    def __del__(self):
        self.close()

    async def _connect(self, host, port):
        url = f'ws://{host}:{port}'
        self.conn = await tornado.websocket.websocket_connect(url)

    def connect(self, address, port):
        fut = asyncio.run_coroutine_threadsafe(self._connect(address, port), self.loop)
        fut.result()

        fut = asyncio.run_coroutine_threadsafe(self.run(), self.loop)
        fut.add_done_callback(run_hook)

    def close(self):
        self.loop.call_soon_threadsafe(self.conn.close)
        self.loop.stop()

    @property
    def hostname(self):
        parts = urllib.parse.urlsplit(self.conn.request.url)
        return parts.hostname

    @property
    def port(self):
        parts = urllib.parse.urlsplit(self.conn.request.url)
        return parts.port

    def on(self, event, callback):
        try:
            callbacks = self.callbacks[event]
        except KeyError:
            callbacks = []
            self.callbacks[event] = callbacks

        callbacks.append(callback)

    def off(self, event, callback):
        callbacks = self.callbacks[event]
        callbacks.remove(callback)

    async def run(self):
        while True:
            msg = await self.conn.read_message()
            if (msg is None):
                if ('close' in self.callbacks):
                    for callback in self.callbacks['close']:
                        callback()
                return

            if isinstance(msg, bytes):
                if (self.vid_session is not None):
                    self.vid_session.add(msg)
            else:
                msg = json.loads(msg)
                buffer_count = msg.get('buffers', 0)

                bufs = []
                for buffer_index in range(buffer_count):
                    buf = await self.conn.read_message()
                    bufs.append(buf)

                event = msg['type']
                if (event == 'remote-call'):
                    self.rpc_session.set(msg['detail'], bufs)
                elif (event in self.callbacks):
                    type, sep, id = event.partition(':')
                    if (type == 'image'):
                        args = (PIL.Image.open(io.BytesIO(bufs[0])),)
                    elif (type == 'cancel'):
                        args = ()
                    else:
                        args = (msg['detail'], bufs)

                    callbacks = self.callbacks[event]
                    for callback in callbacks:
                        callback(*args)

    def new_id(self):
        value = self.next_id
        self.next_id += 1

        return value

    def remote_call(self, method, *args, object_type = None, wait = True, return_buffers = False):
        def func(callback, method, *args):
            id = self.rpc_session.get_id(callback)
            msg = {'detail': {'id': id, 'method': method, 'params': args}}

            self.conn.write_message(json.dumps(msg))

        on_result = RPCCallback(object_type)
        self.loop.call_soon_threadsafe(func, on_result, method, *args)

        if wait:
            on_result.wait()

            if return_buffers:
                return on_result.obj, on_result.bufs

            return on_result.obj

def run_hook(fut):
    e = fut.exception()
    if (e is not None):
        raise e
