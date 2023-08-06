import datetime
import functools
import io
import numbers
import threading
import sys
import time

import PIL.Image

try:
    import IPython
except ImportError:
    pass

from .client_connection import ClientConnection
from .video import av_video

try:
    import ipydingo as ipdg
except ImportError:
    pass

try:
    import zeroconf
except ImportError:
    pass

def astimedelta(period):
    if isinstance(period, datetime.timedelta):
        return period

    if isinstance(period, numbers.Number):
        return datetime.timedelta(seconds = period)

    if isinstance(period, str):
        toks = period.split('.')

        t = datetime.datetime.strptime(toks[0], '%H:%M:%S')
        period = datetime.timedelta(hours = t.hour, minutes = t.minute, seconds = t.second)

        if (len(toks) == 2):
            t_us = datetime.datetime.strptime(toks[1], '%f')
            period += datetime.timedelta(microseconds = t_us.microsecond)

        return period

    raise Error('could not convert to timedelta')

def default_video_factory(hostname, port):
    if ('ipydingo' in sys.modules):
        shell = IPython.get_ipython()
        if ((shell is not None) and ('IPKernelApp' in shell.config)):
            return ipdg.ipy_video(hostname, port)

    return av_video(hostname, port)

class Client(object):
    def __init__(self, host = None, port = None):
        self.conn = None
        self.vid_conns = []

        if (host is None):
            self.autoconnect()
        else:
            if (port is None):
                port = 8080
            self.connect(host, port)

    @property
    def hostname(self):
        return self.conn.hostname

    @property
    def port(self):
        return self.conn.port

    def connect(self, address, port = 8080):
        self.conn = ClientConnection()
        self.conn.on('close', self.close)

        self.conn.connect(address, port)

    def autoconnect(self, type = '_http._tcp.local.'):
        listener = ZeroconfListener('dingo')

        zeroconf_cli = zeroconf.Zeroconf()
        zeroconf_cli.add_service_listener(type, listener)

        listener.wait()
        zeroconf_cli.close()

        self.connect(listener.host, listener.port)

    def close(self):
        while (len(self.vid_conns) > 0):
            vid_conn = self.vid_conns.pop()
            vid_conn.close()

        if (self.conn is not None):
            self.conn.close()
            self.conn = None

    def on(self, event, callback):
        self.conn.on(event, callback)

    def off(self, event, callback):
        self.conn.off(event, callback)

    def remove_listener(self, ev, callback):
        pass

    def camera_brightness(self):
        return self.conn.remote_call('camera_brightness')

    def camera_brightness_range(self):
        return self.conn.remote_call('camera_brightness_range', object_type = tuple)

    def camera_exposure(self):
        return self.conn.remote_call('camera_exposure')

    def camera_exposure_range(self):
        return self.conn.remote_call('camera_exposure_range', object_type = tuple)

    def image(self, callback = None, wait = True):
        def default_callback(im):
            nonlocal res
            res = im

        def cancel_callback():
            self.off(str.format('cancel:{}', id), cancel_callback)
            self.off(str.format('image:{}', id), callback)

            ev.set()

        if (callback is None):
            callback = default_callback

        id = self.conn.new_id()

        self.on(str.format('image:{}', id), callback)
        self.on(str.format('cancel:{}', id), cancel_callback)

        ev = threading.Event()
        res = None
        self.conn.remote_call('image', id)

        if wait:
            ev.wait()

        return res

    def image_every(self, frequency, expiry, callback = None, wait = True):
        @functools.wraps(callback)
        def wrapper(callback):
            def cancel_callback():
                self.off(str.format('cancel:{}', id), cancel_callback)
                self.off(str.format('image:{}', id), callback)

                ev.set()

            id = self.conn.new_id()

            self.on(str.format('image:{}', id), callback)
            self.on(str.format('cancel:{}', id), cancel_callback)

            ev = threading.Event()
            self.conn.remote_call('image_every', id, str(frequency), str(expiry))

            if wait:
                ev.wait()

            return callback

        frequency = astimedelta(frequency)
        expiry = astimedelta(expiry)

        if (callback is None):
            return wrapper

        wrapper(callback)

    def image_background(self):
        obj, bufs = self.conn.remote_call('image_background', return_buffers = True)
        if (len(bufs) == 0):
            return None

        return PIL.Image.open(io.BytesIO(bufs[0]))

    def render_state(self):
        return self.conn.remote_call('render_state')

    def render_z(self):
        return self.conn.remote_call('render_z')

    def state(self):
        return self.conn.remote_call('state')

    def reset_background(self):
        self.conn.remote_call('resetBackground')

    def image_selection(self):
        return self.conn.remote_call('image_selection', object_type = tuple)

    def image_size(self):
        return self.conn.remote_call('image_size')

    def image_size_max(self):
        return self.conn.remote_call('image_size_max')

    def set_camera_brightness(self, value):
        return self.conn.remote_call('set_camera_brightness', value)

    def set_camera_exposure(self, value):
        return self.conn.remote_call('set_camera_exposure', value)

    def set_background_policy(self, value):
        self.conn.remote_call('setBackgroundPolicy', value)

    def set_image_maximized(self):
        self.conn.remote_call('set_image_maximized')

    def set_image_selection(self, value):
        self.conn.remote_call('set_image_selection', value)

    def set_render_state(self, value):
        self.conn.remote_call('set_render_state', value)

    def set_render_remove_background(self, value):
        self.conn.remote_call('set_render_remove_background', value)

    def set_video_resolution(self, value):
        self.conn.remote_call('setVideoResolution', value)

    def save_state(self):
        self.conn.remote_call('save_state')

    def touch(self):
        return self.conn.remote_call('touch')

    def video(self, video_factory = default_video_factory):
        if (video_factory == 'av'):
            video_factory = av_video
        elif (video_factory == 'ipy'):
            video_factory = ipdg.ipy_video

        vid, vid_conn = video_factory(self.hostname, self.port)
        self.vid_conns.append(vid_conn)

        return vid

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close()

class ZeroconfListener(object):
    def __init__(self, name):
        self.name = name
        self.host = None
        self.port = None
        self.ev = threading.Event()

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)

        if (info.get_name() == self.name):
            addresses =  info.parsed_addresses()

            self.host = addresses[0]
            self.port = info.port

            self.ev.set()

    def update_service(self, zeroconf, type, name):
        pass

    def remove_service(self, zeroconf, type, name):
        pass

    def wait(self):
        self.ev.wait()
