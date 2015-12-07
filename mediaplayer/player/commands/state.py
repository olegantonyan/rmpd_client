# -*- coding: utf-8 -*-

import mediaplayer.player.commands.base_command as base


class State(base.BaseCommand):
    def call(self):
        if self._player.isstopped():
            return 'stopped'
        else:
            return 'playing'
