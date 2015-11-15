# -*- coding: utf-8 -*-

import logging

import remotecontrol.protocol.outgoing.base_command as base_command

log = logging.getLogger(__name__)


class PlaybackError(base_command.BaseCommand):
    def call(self, **kwargs):
        message = "{f} ({m})".format(m=kwargs.get('message'), f=kwargs.get('filename'))
        return self._send(self._json(message))

    def _json(self, message):
        return {'type': 'playback', 'status': 'error', 'track': message}

