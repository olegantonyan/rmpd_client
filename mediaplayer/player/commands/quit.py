# -*- coding: utf-8 -*-

import mediaplayer.player.commands.base_command as base


class Quit(base.BaseCommand):
    def call(self):
        self._player.quit()
        self._deinit_player()
        self._set_expected_state('stopped')
        return self._player
