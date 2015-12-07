# -*- coding: utf-8 -*-

import os
import logging
import time

import mediaplayer.player.commands.base_command as base

log = logging.getLogger(__name__)


class PlaybackError(RuntimeError):
    pass


class Play(base.BaseCommand):
    def call(self):
        filename = self._args['filename']
        if filename is None:
            return None
        log.info("start track '%s'", filename)
        if not os.path.isfile(filename):
            log.error("file '{f}' does not exists".format(f=filename))
            # self._run_callback('onerror', message="file does not exists", filename=os.path.basename(filename))
            return None
        try:
            self._try_play(filename)
            self._set_playing_status(True)
            # self._run_callback('onplay', filename=filename)
            return True
        except:
            log.exception("error starting playback")
            # self._run_callback('onerror', message="file does not exists", filename=os.path.basename(filename))
            return False

    def _try_play(self, filename):
            self._player.play(filename)
            retries = 0
            while self._player.isstopped():
                time.sleep(0.5)
                retries += 1
                if retries > 10:
                    raise PlaybackError("unable to start playback after 5 seconds")
