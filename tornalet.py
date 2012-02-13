__author__ = "Gawen Arab"
__copyright__ = "Copyright 2012, Gawen Arab"
__credits__ = ["Gawen Arab"]
__license__ = "Apache License, Version 2.0"
__version__ = "1.0"
__maintainer__ = "Gawen Arab"
__email__ = "g@wenarab.com"
__status__ = "Production"

import greenlet
import tornado.web
import tornado.ioloop
import tornado.httpclient
import time

import functools

def tornalet(method):
    """ Decorator for handler's method to enable tornalet. """
    @functools.wraps(method)
    @tornado.web.asynchronous
    def wrapper(self, *kargs, **kwargs):
        def entry_func():
            method(self, *kargs, **kwargs)

            if not self._finished:
                self.finish()

        greenlet_thread = greenlet.greenlet(entry_func)
        greenlet_thread.switch()

    return wrapper

def asyncify(func = None, callback_argname = None):
    """ Decorator with makes asynchronous a blocking function.
        The parameter callback_argname is the function argument's name for the callback.

        You can use this function in three ways:

        1. As a decorator
        @asyncify
        def blocking_func(..., callback):
            ...

        2. As a decorator, setting the callback argument name
        @asyncify("foo_callback")
        def blocking_func(..., foo_callback):
            ...

        3. Inline
        def blocking_func(..., callback):
            ...

        ret = asyncify(blocking_func)(...)

        NB: an 'asynced' function CAN still be used in blocking mode.
        Just use it normally, tornalet won't do anything.

    """
    if isinstance(func, basestring) or func is None:
        callback_argname = func
        func = None

        def decorator(func):
            return tornadletify(func, callback_argname)

        return decorator

    else:
        callback_argname = callback_argname if callback_argname is not None else "callback"

        @functools.wraps(func)
        def wrapper(*kargs, **kwargs):
            current_greenlet = greenlet.getcurrent()

            # If used in a greenlet context, do the job
            if current_greenlet.parent:
                def switch_callback(ret = None):
                    current_greenlet.switch(ret)

                functools.partial(func, **{callback_argname: switch_callback})(*kargs, **kwargs)

                return current_greenlet.parent.switch()

            else:
                return func(*kargs, **kwargs)

        return wrapper

@asyncify
def sleep(seconds, callback = None):
    """ Sleep for seconds. """
    tornado.ioloop.IOLoop.instance().add_timeout(time.time() + seconds, callback)

@asyncify
def idle(callback):
    """ Idle. Functionally, do nothing, just switch to the ioloop micro-thread. """
    tornado.ioloop.IOLoop.instance().add_callback(callback)

@asyncify
def wait_for_handler(fd, events = None, callback = None):
    """ Wait for the file/socket to be readable and/or writable.

        The parameter events should be a sum of tornado.ioloop.IOLoop.{READ,WRITE,ERROR}.
        If not set, it'll be READ and WRITE.
    """

    events = events if events is not None else tornado.ioloop.IOLoop.READ | tornado.ioloop.IOLoop.WRITE
    def handler_callback(fd, events):
        tornado.ioloop.IOLoop.instance().remove_handler(fd)
        return callback((fd, events))

    tornado.ioloop.IOLoop.instance().add_handler(fd, handler_callback, events)

def wait_for_readable(fd, callback = None):
    """ Wait for the file/socket to be readable. """
    return wait_for_handler(fd, tornado.ioloop.IOLoop.READ, callback)

def wait_for_writable(fd, callback = None):
    """ Wait for the file/socket to be writable. """
    return wait_for_handler(fd, tornado.ioloop.IOLoop.WRITE, callback)

