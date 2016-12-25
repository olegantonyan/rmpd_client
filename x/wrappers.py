# -*- coding: utf-8 -*-

import utils.singleton as singleton


class Wrappers(object, metaclass=singleton.Singleton):
    def __init__(self):
        self._d = None
        self._x = None

    def set_daemon(self, w):
        self._d = w

    def set_x(self, w):
        self._x = w

    def daemon(self):
        return self._d

    def x(self):
        return self._x
