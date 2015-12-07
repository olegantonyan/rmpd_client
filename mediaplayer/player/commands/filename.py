# -*- coding: utf-8 -*-

import mediaplayer.player.commands.base_command as base


class Filename(base.BaseCommand):
    def call(self):
        return self._player.filename()
