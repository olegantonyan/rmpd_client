#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os import path, getcwd

import utils.shell

class Watchdog(object):
    def __init__(self):
        self.__wdt_file = path.join(getcwd(), "watchdogfile")
    
    def feed(self):
        utils.shell.execute("touch {f}".format(f=self.__wdt_file))