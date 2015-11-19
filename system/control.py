# -*- coding: utf-8 -*-

import logging

import utils.shell

log = logging.getLogger(__name__)


class Control(object):
    def reboot(self):
        (r, o, e) = utils.shell.execute("sudo reboot")
        log.debug("reboot return code: {r}\n{o}\n{e}".format(r=r, o=o, e=e))
        return r, o, e
