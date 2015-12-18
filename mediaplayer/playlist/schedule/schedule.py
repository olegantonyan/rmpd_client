# -*- coding: utf-8 -*-

import utils.datetime
import mediaplayer.playlist.schedule.interval as interval


class Schedule(object):
    def __init__(self, items):
        self._items = items
        self._all_times_seconds_sorted_uniq = sorted(list(set(self._all_times_seconds())))

        self._intervals = self._calculate_intervals(self._all_times_seconds_sorted_uniq)
        self._fill_intervals_with_items()

    @property
    def intervals(self):
        return self._intervals

    @property
    def ether_begin_seconds(self):
        return min(self._all_times_seconds_sorted_uniq)

    @property
    def ether_end_seconds(self):
        return max(self._all_times_seconds_sorted_uniq)

    def _fill_intervals_with_items(self):
        for i in self.intervals:
            mean_in_interval_seconds = (i.begin_time_seconds + i.end_time_seconds) / 2
            mean_in_interval_object = utils.datetime.time_from_seconds(mean_in_interval_seconds)
            for j in self._items:
                if j.is_appropriate_at(utils.datetime.datetime_from_time(mean_in_interval_object)):
                    i.add_item(j, self._playbacks_in_interval(j, i))

    def _calculate_intervals(self, all_times_seconds_sorted_uniq):
        return [interval.Interval(value, all_times_seconds_sorted_uniq[index + 1])
                for index, value in enumerate(all_times_seconds_sorted_uniq)
                if index + 1 != len(all_times_seconds_sorted_uniq)]

    def _begin_times_seconds(self):
        return [utils.datetime.time_to_seconds(i.begin_time) for i in self._items]

    def _end_times_seconds(self):
        return [utils.datetime.time_to_seconds(i.end_time) for i in self._items]

    def _all_times_seconds(self):
        return self._begin_times_seconds() + self._end_times_seconds()

    def _time_delta_in_seconds_all_time(self, itm):
        return utils.datetime.time_to_seconds(itm.end_time) - utils.datetime.time_to_seconds(itm.begin_time)

    def _time_delta_in_seconds_interval(self, intvl):
        return intvl.end_time_seconds - intvl.begin_time_seconds

    def _time_delta_outside_intrval(self, itm, intvl):
        return self._time_delta_in_seconds_all_time(itm) - self._time_delta_in_seconds_interval(intvl)

    def _period_in_seconds_all_time(self, itm):
        if itm.playbacks_per_day == 0:
            return 0
        return int(self._time_delta_in_seconds_all_time(itm) / itm.playbacks_per_day)

    def _playbacks_in_interval(self, itm, interval):
        delta = self._time_delta_in_seconds_all_time(itm)
        return self._time_delta_outside_intrval(itm, interval)




