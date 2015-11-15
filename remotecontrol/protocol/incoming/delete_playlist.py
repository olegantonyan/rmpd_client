# -*- coding: utf-8 -*-

import remotecontrol.protocol.incoming.base_command as base_command


class DeletePlaylist(base_command.BaseCommand):
    def call(self):
        print(self.__class__.__name__)
