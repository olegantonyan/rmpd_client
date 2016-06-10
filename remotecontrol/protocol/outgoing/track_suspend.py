# -*- coding: utf-8 -*-

import logging

import remotecontrol.protocol.outgoing.base_command as base_command

log = logging.getLogger(__name__)


class TrackSuspend(base_command.BaseCommand):
    def call(self, **kwargs):
        item = kwargs.get('item')
        if item is None:
            log.error("track is none")
            return
        self._message = self._track_message(item)
        self._message.update({'position_seconds': kwargs.get('position_seconds')})
        return super().call()

