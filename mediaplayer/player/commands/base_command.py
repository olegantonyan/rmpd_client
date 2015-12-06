# -*- coding: utf-8 -*-


class BaseCommand(object):
    def __init__(self, player, **kwargs):
        self._player = player
        self._args = kwargs
