# -*- coding: utf-8 -*-

import logging
import system.systeminfo

import utils.shell as shell

log = logging.getLogger(__name__)


class Control(object):
    def reboot(self):
        (r, o, e) = shell.execute("sudo reboot")
        log.debug("reboot return code: {r}\n{o}\n{e}".format(r=r, o=o, e=e))
        return r, o, e

    def change_timezone(self, tz):
        if 'debian' not in system.systeminfo.linux_disto():
            log.error('cannot change timezone on non-Debian distro')
            return False
        sign = tz[0]
        value = tz[1:3]
        if sign == '+':
            sign = '-'
        elif sign == '-':
            sign = '+'
        posix_gmt_tz = 'Etc/GMT{sign}{value}'.format(sign=sign, value=int(value))
        cli = "sudo sh -c 'echo \"{gmt_tz}\" > /etc/timezone'".format(gmt_tz=posix_gmt_tz)
        (r, o, e) = shell.execute_shell(cli)
        if r != 0:
            log.error('error setting timezone: {e}\n{o}'.format(e=e, o=o))
            return False
        (r, o, e) = shell.execute("sudo dpkg-reconfigure -f noninteractive tzdata")
        if r != 0:
            log.error('error changing timezone: {e}\n{o}'.format(e=e, o=o))
            return False
        log.debug('change timezone result: {r}\n{o}\n{e}'.format(r=r, o=o, e=e))
        return True
