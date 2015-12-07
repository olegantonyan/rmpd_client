# -*- coding: utf-8 -*-

import os
import logging
import time

import mediaplayer.player.commands.base_command as base

log = logging.getLogger(__name__)


class Play(base.BaseCommand):
    def call(self):
        filename = self._args['filename']
        if filename is None:
            return None
        log.info("start track '%s'", filename)
        if not os.path.isfile(filename):
            log.error("file '{f}' does not exists".format(f=filename))
            # self._run_callback('onerror', message="file does not exists", filename=os.path.basename(filename))
            return
        self._set_expected_state('playing', filename=filename)
        self._try_play(filename)
        self._set_playing_status(True)
        # self._run_callback('onplay', filename=filename)

    def _try_play(self, filename):
        try:
            self._player.play(filename)
            retries = 0
            while self._player.isstopped():
                time.sleep(0.5)
                retries += 1
                if retries > 10:
                    msg = 'reinitializing mplayer as it has probably crashed'
                    log.warning(msg)
                    # self._run_callback('onerror', message=msg, filename=os.path.basename(self._playlist.pick_prev()))
                    self._deinit_player()
                    self._init_player()
                    self._player.play(filename)
                    retries = 0
        except:
            log.exception('error starting playback')
