#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from logging import getLogger

log = getLogger(__name__)

import utils.shell


class Control(object):
    def reboot(self):
        (r, o, e) = utils.shell.execute("sudo reboot")
        log.debug("reboot return code: {r}\n{o}\n{e}".format(r=r, o=o, e=e))
        return r, o, e
