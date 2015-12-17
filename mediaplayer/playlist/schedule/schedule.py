# -*- coding: utf-8 -*-

import datetime

import utils.datetime


class Schedule(object):
    def __init__(self, begin_time, end_time, playbacks_per_day):
        self._begin_time = begin_time
        self._end_time = end_time
        self._playbacks_per_day = playbacks_per_day
        self._period_seconds = self.period_in_seconds()
        self._sched_list = []
        self._sched()

    def next_play_time(self, thetime):
        return min(self._sched_list, key=lambda x: x - thetime if x > thetime else datetime.timedelta.max)

    def sched_list(self):
        return self._sched_list

    def period_in_seconds(self):
        if self._playbacks_per_day == 0:
            return 0
        return int(self._time_delta_in_seconds() / self._playbacks_per_day)

    def _sched(self):
        thetime = self._thetime()
        for i in range(self._playbacks_per_day):
            dt = datetime.datetime(year=thetime.year,
                                   month=thetime.month,
                                   day=thetime.day,
                                   hour=self._begin_time.hour,
                                   minute=self._begin_time.minute,
                                   second=self._begin_time.second,
                                   tzinfo=thetime.tzinfo)
            next_play_time = dt + datetime.timedelta(seconds=(self._period_seconds * i))
            self._sched_list.append(next_play_time)

    def _time_delta_in_seconds(self):
        return utils.datetime.time_to_seconds(self._end_time) - utils.datetime.time_to_seconds(self._begin_time)

    def _thetime(self):
        return utils.datetime.now()
