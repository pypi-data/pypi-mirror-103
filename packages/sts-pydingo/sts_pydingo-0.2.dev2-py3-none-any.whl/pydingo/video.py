import importlib
import queue

try:
    import av
except ImportError:
    pass

from .client_connection import ClientConnection

class QueueIO(object):
    def __init__(self):
        self.finished = False
        self.queue = queue.Queue()

    def read(self, n):
#        print('read(%d)' % n)
        if self.finished:
            return b''

        data = self.queue.get()
        if not data:
            self.finished = True
        assert len(data) <= n
        return data

    def write(self, buf):
        self.queue.put(buf)

class VideoSession(object):
    def __init__(self):
        self.qio = QueueIO()

    def add(self, buf):
        self.qio.write(buf)

def av_video(hostname, port):
    conn = ClientConnection()
    conn.vid_session = VideoSession()

    conn.connect(hostname, port)
    conn.remote_call('video', conn.new_id())

    return av.open(conn.vid_session.qio), conn
