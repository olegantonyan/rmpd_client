# -*- coding: utf-8 -*-

import remotecontrol.protocol.outgoing.base_command as base_command


class UpdatePlaylist(base_command.BaseCommand):
    def call(self, **kwargs):
        files = kwargs.get('files') or []
        self._message = ', '.join(files)
        return super().call()
