# -*- coding: utf-8 -*-

import mediaplayer.player.commands.base_command as base


class TimePos(base.BaseCommand):
    def call(self):
        return self._player.time_pos()
