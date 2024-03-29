# -*- coding: utf-8 -*-

import logging

import remotecontrol.protocol.incoming.base_command as base_command
import system.control as control
import utils.config as config

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

        mqsp = self._data.get('message_queue_sync_period')
        if mqsp is not None:
            ok, cmsg = self._set_message_queue_sync_period(mqsp)
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

    def _set_message_queue_sync_period(self, mqsp):
        log.info('changing message queue sync period to {p} hours'.format(p=mqsp))
        config.Config().set_message_queue_sync_period(int(mqsp))
        return True, 'message queue sync period set to {m}'.format(m=mqsp)
