#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import hardware
import system.control


class System(object):
    def restart_network(self):
        return hardware.platfrom.restart_networking()

    def reboot(self):
        (r, o, e) = system.control.Control().reboot()
        return o
