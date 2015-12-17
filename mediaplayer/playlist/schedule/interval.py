# -*- coding: utf-8 -*-

import utils.datetime


class Interval(object):
    def __init__(self, begin_time_seconds, end_time_seconds):
        self._begin_time_seconds = begin_time_seconds
        self._end_time_seconds = end_time_seconds
        self._items = []

    def add_item(self, i):
        self._items.append(i)

    @property
    def items(self):
        return self._items

    @property
    def begin_time_seconds(self):
        return self._begin_time_seconds

    @property
    def end_time_seconds(self):
        return self._end_time_seconds

    @property
    def begin_time_object(self):
        return utils.datetime.time_from_seconds(self.begin_time_seconds)

    @property
    def end_time_object(self):
        return utils.datetime.time_from_seconds(self.end_time_seconds)

    def __str__(self):
        return "{b}-{e} {itms}".format(b=utils.datetime.time_to_string(self.begin_time_object),
                                       e=utils.datetime.time_to_string(self.end_time_object),
                                       itms=self.items)

    def __repr__(self):
        return self.__str__()
