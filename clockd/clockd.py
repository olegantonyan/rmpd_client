#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import ntplib
import time
import random

import system.control as control

log = logging.getLogger(__name__)


class Clockd(object):
    NTP_SERVERS = ['0.debian.pool.ntp.org', '1.debian.pool.ntp.org', '2.debian.pool.ntp.org', '3.debian.pool.ntp.org',
                   '0.opensuse.pool.ntp.org', '1.opensuse.pool.ntp.org', '2.opensuse.pool.ntp.org', '3.opensuse.pool.ntp.org',
                   '0.pool.ntp.org', '1.pool.ntp.org', '2.pool.ntp.org', '3.pool.ntp.org', 'time.windows.com', 'pool.ntp.org',
                   '0.ru.pool.ntp.org', '1.ru.pool.ntp.org', '2.ru.pool.ntp.org', '3.ru.pool.ntp.org']

    def __init__(self):
        self._stop_flag = False
        self._once_syncronized = False

    def run(self):
        while not self._stop_flag:
            ntp_time = self._ntp_time()
            if ntp_time:
                log.info("NTP time synchronized: {}".format(ntp_time))
                self._save_time(ntp_time)
                self._once_syncronized = True

            if self._once_syncronized:
                time.sleep(86400)
            else:
                time.sleep(2)

    def _ntp_time(self):
        client = ntplib.NTPClient()
        servers = list(self.NTP_SERVERS)
        while len(servers) > 0:
            server = random.choice(servers)
            try:
                response = client.request(server, version=3)
                return time.ctime(response.tx_time)
            except Exception as e:
                log.debug(str(e))
                servers.remove(server)
        return None

    def _save_time(self, tm):
        c = control.Control()
        if c.set_time(tm) and not self._once_syncronized:
            c.set_hwclock_to_system_time()

    def __del__(self):
        self._stop_flag = True
