# -*- coding: utf-8 -*-

import logging

import remotecontrol.protocol.outgoing.base_command as base_command

log = logging.getLogger(__name__)


class TrackEnd(base_command.BaseCommand):
    def call(self, **kwargs):
        item = kwargs.get('item')
        if item is None:
            log.error("track is none")
            return
        self._message = self._track_message(item)
        return super().call()

