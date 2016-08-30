#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import time

import utils.shell as shell
import hardware

log = logging.getLogger(__name__)


class HdmiHotplug(object):
    def __init__(self, onchange_callback=None):
        self._stop_flag = False
        self._prev_monitor = ''
        self._callback = onchange_callback

    def run(self):
        if hardware.platfrom.__name__ != 'raspberry':
            return
        while not self._stop_flag:
            try:
                current_monitor = self._read_monitor_name()
                if current_monitor != self._prev_monitor:
                    log.info("monitor has changed '{p}' -> '{n}'".format(p=self._prev_monitor, n=current_monitor))
                    self._prev_monitor = current_monitor
                    if self._is_monitor_present(current_monitor):
                        self._set_preferred_mode()
                        current_status = self._read_status()
                        resolution = current_status.split("@")[0].split(" ")[-2]
                        xres = resolution.split("x")[0]
                        yres = resolution.split("x")[1]
                        log.info("setting framebuffer resolution to {}".format(resolution))
                        self._set_framebuffer_resolution(xres, yres)
                        self._run_callback()
            except:
                log.exception("error running hdmi hotplug loop")
            finally:
                time.sleep(5)

    def _run_callback(self):
        if self._callback is not None:
            self._callback()

    def _read_monitor_name(self):
        (r, o, e) = shell.execute("sudo tvservice -n")
        if r != 0:
            raise RuntimeError("error getting info about connected monitors: {e}\n{o}".format(e=e, o=o))
        return o.strip()

    def _set_preferred_mode(self):
        (r, o, e) = shell.execute("sudo tvservice -p")
        if r != 0:
            raise RuntimeError("error setting preferrend mode: {e}\n{o}".format(e=e, o=o))

    def _read_status(self):
        (r, o, e) = shell.execute("sudo tvservice -s")
        if r != 0:
            raise RuntimeError("error getting current hdmi status: {e}\n{o}".format(e=e, o=o))
        return o.strip()

    def _set_framebuffer_resolution(self, x, y):
        (r, o, e) = shell.execute("sudo fbset -xres {x} -yres {y}".format(x=x, y=y))
        if r != 0:
            raise RuntimeError("error setting framebuffer resolution to {x}x{y}: {e}\n{o}".format(x=x, y=y, e=e, o=o))

    def _is_monitor_present(self, name):
        return "No device present" not in name and name != ''

