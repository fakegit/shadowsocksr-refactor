#!/usr/bin/python
# -*- coding:utf-8 -*-

"""
 @author: clowwindy
 @modify: valor.
 @file: eventloop.py

 Copyright 2013-2015 clowwindy
 Copyright 2019 valord577

 Licensed under the Apache License, Version 2.0 (the "License"); you may
 not use this file except in compliance with the License. You may obtain
 a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 License for the specific language governing permissions and limitations
 under the License.
"""

# from ssloop
# https://github.com/clowwindy/ssloop

import os
import time
import socket
import select
import errno
import logging
# -- import from shadowsockesr-v
import exit


POLL_NULL = 0x00
POLL_IN = select.EPOLLIN
POLL_OUT = select.EPOLLOUT
POLL_ERR = select.EPOLLERR
POLL_HUP = select.EPOLLHUP
POLL_NVAL = select.POLLNVAL


EVENT_NAMES = {
    POLL_NULL: 'POLL_NULL',
    POLL_IN: 'POLL_IN',
    POLL_OUT: 'POLL_OUT',
    POLL_ERR: 'POLL_ERR',
    POLL_HUP: 'POLL_HUP',
    POLL_NVAL: 'POLL_NVAL',
}

# we check timeouts every TIMEOUT_PRECISION seconds
TIMEOUT_PRECISION = 2


class EventLoop:

    _instance = None

    # singleton
    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        # only support Linux and require 'epoll' model.
        if hasattr(select, 'epoll'):
            self.epoll = select.epoll()
            logging.info('Using event model: epoll.')
        else:
            exit.error('Only support Linux and require \'epoll\' model.')

        self._fdmap = {}  # (f, handler)
        self._last_time = time.time()
        self._periodic_callbacks = []
        self._stopping = False

    def poll(self, timeout=None):
        events = self.epoll.poll(timeout)
        return [(self._fdmap[fd][0], fd, event) for fd, event in events]

    def add(self, socks, mode, handler):
        fd = socks.fileno()
        self._fdmap[fd] = (socks, handler)
        self.epoll.register(fd, mode)

    def remove(self, socks):
        fd = socks.fileno()
        del self._fdmap[fd]
        self.epoll.unregister(fd)

    def removefd(self, fd):
        del self._fdmap[fd]
        self.epoll.unregister(fd)

    def add_periodic(self, callback):
        self._periodic_callbacks.append(callback)

    def remove_periodic(self, callback):
        self._periodic_callbacks.remove(callback)

    def modify(self, f, mode):
        fd = f.fileno()
        self.epoll.modify(fd, mode)

    def stop(self):
        self._stopping = True

    def run(self):
        events = []
        while not self._stopping:
            asap = False
            try:
                events = self.poll(TIMEOUT_PRECISION)
            except (OSError, IOError) as e:
                if errno_from_exception(e) in (errno.EPIPE, errno.EINTR):
                    # EPIPE: Happens when the client closes the connection
                    # EINTR: Happens when received a signal
                    # handles them as soon as possible
                    asap = True
                    logging.debug('poll:%s', e)
                else:
                    logging.error('poll:%s', e)
                    import traceback
                    traceback.print_exc()
                    continue

            handle = False
            for sock, fd, event in events:
                handler = self._fdmap.get(fd, None)
                if handler is not None:
                    handler = handler[1]
                    try:
                        handle = handler.handle_event(sock, fd, event) or handle
                    except (OSError, IOError) as e:
                        logging.error(e)
            now = time.time()
            if asap or now - self._last_time >= TIMEOUT_PRECISION:
                for callback in self._periodic_callbacks:
                    callback()
                self._last_time = now
            if events and not handle:
                time.sleep(0.001)

    def __del__(self):
        self.epoll.close()


# from tornado
def errno_from_exception(e):
    """Provides the errno from an Exception object.

    There are cases that the errno attribute was not set so we pull
    the errno out of the args but if someone instatiates an Exception
    without any args you will get a tuple error. So this function
    abstracts all that behavior to give you a safe way to get the
    errno.
    """

    if hasattr(e, 'errno'):
        return e.errno
    elif e.args:
        return e.args[0]
    else:
        return None


# from tornado
def get_sock_error(sock):
    error_number = sock.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)
    return socket.error(error_number, os.strerror(error_number))
