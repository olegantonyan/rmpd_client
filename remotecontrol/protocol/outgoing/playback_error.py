# -*- coding: utf-8 -*-

import logging

import remotecontrol.protocol.outgoing.base_command as base_command

log = logging.getLogger(__name__)


class PlaybackError(base_command.BaseCommand):
    def call(self, **kwargs):
        item = kwargs.get('item')
        if item is None:
            log.error("track is none")
            return

        msg = self._track_message(item)
        msg.update({'error_text': kwargs.get('message')})
        self._message = msg
        return super().call()


