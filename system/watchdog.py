# -*- coding: utf-8 -*-

import os

import utils.shell as shell


class Watchdog(object):
    def __init__(self):
        self._wdt_file = os.path.join(os.getcwd(), "watchdogfile")

    def feed(self):
        shell.execute("touch {f}".format(f=self._wdt_file))
