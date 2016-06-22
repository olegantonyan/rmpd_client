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
        try:
            self.remount_rootfs()
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
        finally:
            self.remount_rootfs(False)

    def is_rootfs_readonly(self):
        (r, o, e) = shell.execute_shell('mount | grep "on / type ext4 (ro,"')
        return len(o) > 0

    def remount_rootfs(self, rw=True):
        log.debug('remount rootfs')
        if not rw and self.is_rootfs_readonly():
            log.debug('rootfs is already read-only')
            return True
        if rw and not self.is_rootfs_readonly():
            log.debug('rootfs is already read-write')
            return True
        (r, o, e) = shell.execute("sudo mount -o remount,{mode} /".format(mode=('rw' if rw else 'ro')))
        if r != 0:
            log.error('fs remount failed: {e}\n{o}'.format(e=e, o=o))
        return r == 0

    def is_hwclock_present(self):
        (r, o, e) = shell.execute("sudo hwclock -r")
        return r == 0

    def set_time(self, tm):
        log.debug("set the time to {}".format(tm))
        (r, o, e) = shell.execute_shell('sudo date -s "{}"'.format(tm))
        if r != 0:
            log.error("error setting the time: {e}\n{o}".format(e=e, o=o))
        return r == 0

    def set_hwclock_to_system_time(self):
        log.debug("setting hwclock to system time")
        if not self.is_hwclock_present():
            return False
        self.remount_rootfs(True)
        (r, o, e) = shell.execute("sudo hwclock -w")
        self.remount_rootfs(False)
        if r != 0:
            log.error("error setting hardware clock to system time: {e}\n{o}".format(e=e, o=o))
        return r == 0

