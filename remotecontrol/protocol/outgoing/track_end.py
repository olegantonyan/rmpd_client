# -*- coding: utf-8 -*-

import logging

import remotecontrol.protocol.outgoing.base_command as base_command

log = logging.getLogger(__name__)


class TrackEnd(base_command.BaseCommand):
    def call(self, **kwargs):
        filename = kwargs.get('filename')
        if filename is None:
            log.error("track is none")
            return
        return self._send(self._json(filename))

    def _json(self, filename):
        return {'type': 'playback', 'status': 'end', 'track': filename}
