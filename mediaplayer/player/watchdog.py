# -*- coding: utf-8 -*-

import logging

log = logging.getLogger(__name__)


class Watchdog(object):
    def __init__(self):
        self._last_resume_position = None

    def resumed_at(self, time_pos):
        self._last_resume_position = int(time_pos)

    def is_ok_to_resume(self, time_pos):
        if self._last_resume_position is None:
            return True
        time_pos = int(time_pos)
        log.info("is ok to resume {one} - {two}".format(one=self._last_resume_position, two=time_pos))
        return self._last_resume_position != time_pos

    def reset(self):
        self._last_resume_position = None
