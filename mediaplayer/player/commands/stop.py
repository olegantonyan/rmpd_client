# -*- coding: utf-8 -*-

import logging

import mediaplayer.player.commands.base_command as base

log = logging.getLogger(__name__)


class Stop(base.BaseCommand):
    def call(self):
        log.info('stopped')
        self._set_playing_status(False)
        self._player.stop()
        return True
