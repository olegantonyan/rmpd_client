# -*- coding: utf-8 -*-

import logging

import remotecontrol.protocol.outgoing.base_command as base_command

log = logging.getLogger(__name__)


class PlaybackError(base_command.BaseCommand):
    def call(self, **kwargs):
        self._message = "{f} ({m})".format(m=kwargs.get('message'), f=kwargs.get('filename'))
        return super().call()


