# -*- coding: utf-8 -*-


import remotecontrol.protocol.commands.base_command as base_command


class UpdatePlaylist(base_command.BaseCommand):
    def call(self):
        print(self.__class__.__name__)
