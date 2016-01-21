# -*- coding: utf-8 -*-

import logging

import remotecontrol.protocol.incoming.base_command as base_command
import system.control as control

log = logging.getLogger(__name__)


class UpdateSetting(base_command.BaseCommand):
    def call(self):
        tz = self._data['time_zone']
        log.info('changing device timezone to {nz}'.format(nz=tz))
        if control.Control().change_timezone(tz):
            self._sender('ack_ok').call(sequence=self._sequence, message='timezone has been changed to {tz}'.format(tz=tz))
        else:
            self._sender('ack_fail').call(sequence=self._sequence, message='error changing timezone to {tz}'.format(tz=tz))
