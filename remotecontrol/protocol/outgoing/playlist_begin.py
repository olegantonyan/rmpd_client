# -*- coding: utf-8 -*-

import logging

import remotecontrol.protocol.outgoing.base_command as base_command

log = logging.getLogger(__name__)


class PlaylistBegin(base_command.BaseCommand):
    def call(self, **kwargs):
        files = kwargs.get('files')
        return self._send(self._json(files))

    def _json(self, files):
        return {'type': 'playback', 'status': 'begin_playlist', 'track': files}