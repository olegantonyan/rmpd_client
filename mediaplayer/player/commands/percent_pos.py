# -*- coding: utf-8 -*-

import mediaplayer.player.commands.base_command as base


class PercentPos(base.BaseCommand):
    def call(self):
        return self._player.percent_pos()
