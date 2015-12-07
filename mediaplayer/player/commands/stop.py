# -*- coding: utf-8 -*-

import logging

import mediaplayer.player.commands.base_command as base

log = logging.getLogger(__name__)


class Stop(base.BaseCommand):
    def call(self):
        log.info('stopped')
        self._set_expected_state('stopped')
        return self._player.stop()
        # self._run_callback('onstop', filename=os.path.basename(self._playlist.current()))
