# -*- coding: utf-8 -*-

import os
import logging
import time

import mediaplayer.player.commands.base_command as base

log = logging.getLogger(__name__)


class Play(base.BaseCommand):
    def call(self):
        filepath = self._args['filepath']
        if filepath is None:
            return False
        log.info("start track '%s'", filepath)
        if not os.path.isfile(filepath):
            log.error("file '{f}' does not exists".format(f=filepath))
            return False
        self._try_play(filepath)
        self._set_playing_status(True)
        return True

    def _try_play(self, filepath):
            self._player.play(filepath)
            retries = 0
            while self._player.isstopped():
                time.sleep(0.5)
                retries += 1
                if retries > 10:
                    raise base.PlayerError("unable to start playback after 5 seconds")
            return True
