#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from threading import Thread, Timer

def run_in_thread(target, args, daemon=True):
    t = Thread(target=target, args=args)  
    t.setDaemon(daemon)
    t.start()
    return t

def run_after_timeout(timeout, target, daemon=True):
    t = Timer(timeout, target)
    t.setDaemon(daemon)
    t.start()
    return t