# -*- coding: utf-8 -*-

import system.status


class PlayerError(RuntimeError):
    pass


class BaseCommand(object):
    def __init__(self, player_getter, **kwargs):
        self._player_getter = player_getter
        self._args = kwargs

    @property
    def _player(self):
        return self._player_getter()

    def _set_playing_status(self, status):
        system.status.Status().playing = status
