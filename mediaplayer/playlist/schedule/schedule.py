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
        for j in self._items:
            self._fill_playbacks_in_intervals(j)

    def _calculate_intervals(self, all_times_seconds_sorted_uniq):
        return [interval.Interval(value, all_times_seconds_sorted_uniq[index + 1])
                for index, value in enumerate(all_times_seconds_sorted_uniq)
                if index + 1 != len(all_times_seconds_sorted_uniq)]

    def _begin_times_seconds(self):
        return [self._time_to_seconds(i.begin_time) for i in self._items]

    def _end_times_seconds(self):
        return [self._time_to_seconds(i.end_time) for i in self._items]

    def _time_to_seconds(self, tm):
        return utils.datetime.time_to_seconds(tm)

    def _all_times_seconds(self):
        return self._begin_times_seconds() + self._end_times_seconds()

    def _fill_playbacks_in_intervals(self, itm):
        times_in_item_play_time = list(filter(lambda x:
                                              self._time_to_seconds(itm.begin_time) <= x <= self._time_to_seconds(itm.end_time),
                                              self._all_times_seconds_sorted_uniq))
        fit_intrevals = self._calculate_intervals(times_in_item_play_time)
        if fit_intrevals[0].begin_time_object != itm.begin_time or fit_intrevals[-1].end_time_object != itm.end_time:
            raise RuntimeError('item {i} does not fit into intervals ({b}..{e})'.format(i=itm, b=fit_intrevals[0], e=fit_intrevals[-1]))
        if itm.playbacks_per_day == 0:
            return
        all_time_seconds = fit_intrevals[-1].end_time_seconds - fit_intrevals[0].begin_time_seconds
        all_time_period = round(all_time_seconds / itm.playbacks_per_day)
        for j in fit_intrevals:
            intrval_playbacks = round((j.end_time_seconds - j.begin_time_seconds) / all_time_period)
            for i in self._intervals:
                if i.begin_time_seconds == j.begin_time_seconds and i.end_time_seconds == j.end_time_seconds:
                    i.add_item(itm, intrval_playbacks)




