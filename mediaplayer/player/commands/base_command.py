# -*- coding: utf-8 -*-

import system.status


class BaseCommand(object):
    def __init__(self, player_getter, init_player_cb, deinit_player_cb, **kwargs):
        self._player_getter = player_getter
        self._init_player = init_player_cb
        self._deinit_player = deinit_player_cb
        self._args = kwargs

    @property
    def _player(self):
        return self._player_getter()

    def _set_playing_status(self, status):
        system.status.Status().playing = status

