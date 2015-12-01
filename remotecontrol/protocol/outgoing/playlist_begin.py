# -*- coding: utf-8 -*-

import logging

import remotecontrol.protocol.outgoing.base_command as base_command

log = logging.getLogger(__name__)


class PlaylistBegin(base_command.BaseCommand):
    def call(self, **kwargs):
        files = kwargs.get('files')
        self._message = ', '.join(files)
        return super().call()
