# -*- coding: utf-8 -*-

import logging

import remotecontrol.protocol.incoming.base_command as base_command
import system.control as control

log = logging.getLogger(__name__)


class UpdateSetting(base_command.BaseCommand):
    def call(self):
        msg = ''
        all_ok = True
        tz = self._data.get('time_zone')
        if tz is not None:
            ok, cmsg = self._change_timezone(tz)
            msg += ';' + cmsg
            all_ok = all_ok and ok
        return self._ack(all_ok, msg)

    def _change_timezone(self, tz):
        log.info('changing device timezone to {nz}'.format(nz=tz))
        ok = control.Control().change_timezone(tz)
        if ok:
            msg = 'timezone has been changed to {tz}'.format(tz=tz)
        else:
            msg = 'error changing timezone to {tz}'.format(tz=tz)
        return ok, msg