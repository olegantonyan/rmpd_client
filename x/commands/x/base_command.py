# -*- coding: utf-8 -*-


class BaseCommand(object):
    def __init__(self, data, **kwargs):
        self._window = kwargs['window']
        self._data = data
