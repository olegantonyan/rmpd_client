# -*- coding: utf-8 -*-

import remotecontrol.protocol.outgoing.base_command as base_command


class PowerOn(base_command.BaseCommand):
    def call(self):
        return self._send(self._json())

    def _json(self):
        return {'type': 'power', 'status': 'on'}
