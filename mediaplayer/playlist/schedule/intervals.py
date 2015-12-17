# -*- coding: utf-8 -*-

import utils.datetime
import mediaplayer.playlist.schedule.interval as interval


class Intervals(object):
    def __init__(self, items):
        self._items = items
        begin_times_seconds = [utils.datetime.time_to_seconds(i.begin_time) for i in self._items]
        end_times_seconds = [utils.datetime.time_to_seconds(i.end_time) for i in self._items]
        all_times_seconds = begin_times_seconds + end_times_seconds
        all_times_seconds_sorted_uniq = sorted(list(set(all_times_seconds)))

        self._intervals = [interval.Interval(value, all_times_seconds_sorted_uniq[index + 1])
                           for index, value in enumerate(all_times_seconds_sorted_uniq)
                           if index + 1 != len(all_times_seconds_sorted_uniq)]
        self._fill_intervals_with_items()

    @property
    def intervals(self):
        return self._intervals

    def _fill_intervals_with_items(self):
        for i in self.intervals:
            mean_in_interval_seconds = (i.begin_time_seconds + i.end_time_seconds) / 2
            mean_in_interval_object = utils.datetime.time_from_seconds(mean_in_interval_seconds)
            for j in self._items:
                if j.is_appropriate_at(utils.datetime.datetime_from_time(mean_in_interval_object)):
                    i.add_item(j)





