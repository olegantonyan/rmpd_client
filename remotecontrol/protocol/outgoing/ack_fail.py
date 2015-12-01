# -*- coding: utf-8 -*-

import remotecontrol.protocol.outgoing.base_command as base_command


class AckFail(base_command.BaseCommand):
    def call(self, **kwargs):
        self._message = kwargs.get('message') or ''
        self._sequence = kwargs.get('sequence') or 0
        return super().call()
