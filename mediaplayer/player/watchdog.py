# -*- coding: utf-8 -*-

import logging

log = logging.getLogger(__name__)


class Watchdog(object):
    def __init__(self):
        self._last = (None, None)

    def resumed_at(self, item, time_pos):
        time_pos = int(time_pos)
        self._last = (item, time_pos)

    def is_ok_to_resume(self, item, time_pos):
        if self._last[0] is None or self._last[1] is None:
            return True
        time_pos = int(time_pos)
        # log.info("is ok to resume {one} - {two}".format(one=self._last[1], two=time_pos))
        if self._last[0] != item:
            return True
        return self._last[1] != time_pos

    def reset(self):
        self._last = (None, None)
