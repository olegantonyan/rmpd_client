# -*- coding: utf-8 -*-

import remotecontrol.protocol.outgoing.base_command as base_command


class UpdatePlaylist(base_command.BaseCommand):
    def call(self, **kwargs):
        files = kwargs.get('files') or []
        return self._send(self._json(files))

    def _json(self, files):
        return {'type': 'playback', 'status': 'update_playlist', 'track': files}
