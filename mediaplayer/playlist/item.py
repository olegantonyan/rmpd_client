# -*- coding: utf-8 -*-

import datetime


class Item(object):
    def __init__(self, i):
        self._d = i

    @property
    def filename(self):
        return self._d['filename']

    @property
    def id(self):
        return self._d['id']

    @property
    def type(self):
        return self._d['type']

    @property
    def position(self):
        return self._d['position']

    @property
    def begin_time(self):
        return self._parse_time(self._d['begin_time'])

    @property
    def end_time(self):
        return self._parse_time(self._d['end_time'])

    @property
    def begin_date(self):
        return self._parse_date(self._d['begin_date'])

    @property
    def end_date(self):
        return self._parse_date(self._d['end_date'])

    @property
    def playbacks_per_day(self):
        return self._d['playbacks_per_day']

    def is_background(self):
        return self.type == 'background'

    def is_advertising(self):
        return self.type == 'advertising'

    def is_appropriate_at(self, thetime):
        if self.is_advertising():
            return False
        return self.begin_time <= thetime <= self.end_time

    @property
    def playbacks_per_hour(self):
        if self.is_background():
            return 0
        begin_hour = self.begin_time.hour
        end_hour = self.end_time.hour
        return self.playbacks_per_day / (end_hour - begin_hour)

    def _parse_time(self, arg):
        if arg is None:
            return None
        return datetime.datetime.strptime(arg, '%H:%M:%S').time()

    def _parse_date(self, arg):
        if arg is None:
            return None
        return datetime.datetime.strptime(arg, '%Y-%m-%d').date()
