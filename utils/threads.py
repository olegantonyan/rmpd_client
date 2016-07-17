# -*- coding: utf-8 -*-

import threading
import logging
import traceback


log = logging.getLogger(__name__)


def run_in_thread(target, args=(), daemon=True):
    t = threading.Thread(target=target, args=args)
    t.setDaemon(daemon)
    t.start()
    return t


def run_after_timeout(timeout, target, daemon=True):
    t = threading.Timer(timeout, target)
    t.setDaemon(daemon)
    t.start()
    return t


def synchronized(lock, timeout=5):
    def wrap(f):
        def new_func(*args, **kw):
            acquired = lock.acquire(timeout=timeout)
            if not acquired:
                log.error("failed to acquire lock after {timeout} seconds\n{stack}".format(timeout=timeout, stack='\n'.join(traceback.format_stack())))
                log.error("function '{}' will be called without a lock!".format(f.__name__))
            result = f(*args, **kw)
            if acquired:
                lock.release()
            return result
        return new_func
    return wrap
