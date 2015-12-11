# -*- coding: utf-8 -*-

import datetime

import utils.files


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

    @property
    def is_background(self):
        return self.type == 'background'

    @property
    def is_advertising(self):
        return self.type == 'advertising'

    def is_appropriate_at(self, thetime):
        fit_time = lambda: self.begin_time <= thetime.time() <= self.end_time
        fit_date = lambda: self.begin_date <= thetime.date() <= self.end_date
        if self.is_advertising:
            return fit_time() and fit_date()
        else:
            return fit_time()

    @property
    def playbacks_per_hour(self):
        if self.is_background:
            return 0
        begin_hour = self.begin_time.hour
        end_hour = self.end_time.hour
        return self.playbacks_per_day / (end_hour - begin_hour)

    @property
    def filepath(self):
        return utils.files.full_file_localpath(self.filename)

    def _parse_time(self, arg):
        if arg is None:
            return None
        return datetime.datetime.strptime(arg, '%H:%M:%S').time()

    def _parse_date(self, arg):
        if arg is None:
            return None
        return datetime.datetime.strptime(arg, '%Y-%m-%d').date()
