# -*- coding: utf-8 -*-

import threading


def run_in_thread(target, args, daemon=True):
    t = threading.Thread(target=target, args=args)
    t.setDaemon(daemon)
    t.start()
    return t


def run_after_timeout(timeout, target, daemon=True):
    t = threading.Timer(timeout, target)
    t.setDaemon(daemon)
    t.start()
    return t
