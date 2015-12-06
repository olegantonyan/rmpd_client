# -*- coding: utf-8 -*-

import mediaplayer.player.commands.base_command as base


class Play(base.BaseCommand):
    def call(self):
        print("YEOP")
        return 'hello'
