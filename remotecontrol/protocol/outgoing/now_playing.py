# -*- coding: utf-8 -*-

import os

import remotecontrol.protocol.outgoing.base_command as base_command


class NowPlaying(base_command.BaseCommand):
    def call(self, **kwargs):
        track = kwargs.get('track') or 'nothing'
        percent_position = kwargs.get('percent_position') or 0
        message = "{name} ({c}%)".format(name=os.path.basename(str(track)), c=str(percent_position))
        self._queued = False
        return self._send(self._json(message))

    def _json(self, message):
        return {'type': 'playback', 'status': 'now_playing', 'track': message}
