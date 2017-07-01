# -*- coding: utf-8 -*-

import logging
import time

import hardware
import system.status as status

log = logging.getLogger(__name__)


class Networkd(object):
    def __init__(self):
        self._stop_flag = False

    def run(self):
        offline_counter = 0
        while not self._stop_flag:
            if status.Status().online:
                offline_counter = 0
            else:
                offline_counter += 1

            if offline_counter >= 20:
                log.info('been offline for too long, restarting network')
                hardware.platfrom.restart_networking()
                offline_counter = 0

            time.sleep(60)

    def __del__(self):
        self._stop_flag = True
