import asyncio

class RPCError(Exception):
    def __init__(self, message, code):
        Exception.__init__(self, message)

        self.code = code

class RPCSession(object):
    def __init__(self):
        self.next_id = 0
        self.futs = {}

    def get_id(self, callback = None):
        value = self.next_id
        self.next_id += 1

        loop = asyncio.get_event_loop()

        fut = loop.create_future()
        if (callback is not None):
            fut.add_done_callback(lambda fut: callback(fut.result()))

        self.futs[value] = fut

        return value

    def set_result(self, id, value):
        fut = self.futs.pop(id)
        fut.set_result(value)

    def set_error(self, id, value):
        raise RPCError(**value)

    def set(self, dtl, bufs):
        if ('error' in dtl):
            self.set_error(dtl['error'])
        else:
            self.set_result(dtl['id'], (dtl['result'], bufs))
