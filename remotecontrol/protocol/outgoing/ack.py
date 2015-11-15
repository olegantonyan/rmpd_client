# -*- coding: utf-8 -*-

import remotecontrol.protocol.outgoing.base_command as base_command


class Ack(base_command.BaseCommand):
    def call(self, **kwargs):
        ok = kwargs.get('ok') or False
        message = kwargs.get('message') or ''
        self._sequence = kwargs.get('sequence') or 0
        self._queued = True
        self._send(self._json(ok, message))

    def _json(self, ok, message):
        return {'type': 'ack', 'status': 'ok' if ok else 'fail', 'message': message}
