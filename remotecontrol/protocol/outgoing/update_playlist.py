# -*- coding: utf-8 -*-

import remotecontrol.protocol.outgoing.base_command as base_command


class UpdatePlaylist(base_command.BaseCommand):
    def call(self, **kwargs):
        files = kwargs.get('files') or []
        max_sz = 20
        sz = len(files)
        if sz > max_sz:
            files = files[0:max_sz]
            files.append('... and {c} more'.format(c=sz - max_sz))
        self._message = ', '.join(files)
        return super().call()
