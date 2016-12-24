# -*- coding: utf-8 -*-

_gdw = None


def save(daemon_wrapper):
    global _gdw
    _gdw = daemon_wrapper


def get():
    return _gdw
