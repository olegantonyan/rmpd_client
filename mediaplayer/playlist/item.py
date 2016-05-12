# -*- coding: utf-8 -*-

import datetime

import utils.files as files
import utils.datetime


def parse_time(arg):
    if arg is None:
        return None
    return datetime.datetime.strptime(arg, '%H:%M:%S').time()


def parse_date(arg):
    if arg is None:
        return None
    return datetime.datetime.strptime(arg, '%d.%m.%Y').date()


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
        return parse_time(self._d['begin_time'])

    @property
    def end_time(self):
        return parse_time(self._d['end_time'])

    @property
    def begin_date(self):
        return parse_date(self._d['begin_date'])

    @property
    def end_date(self):
        return parse_date(self._d['end_date'])

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
        return self._fit_time(thetime) and self._fit_date(thetime)

    def is_required_at(self, thetime):
        if not self.is_advertising:
            return False
        now = utils.datetime.time_to_seconds(thetime)
        low = now - 2
        high = low + 2
        for i in self.schedule_at(thetime):
            if low <= utils.datetime.time_to_seconds(i) <= high:
                return True
        return False

    @property
    def filepath(self):
        return files.full_file_localpath(self.filename)

    @property
    def schedule_intervals(self):
        return [ScheduleInterval(i) for i in self._d['schedule_intervals']]

    def schedule_at(self, date):
        for i in self.schedule_intervals:
            if i.date_interval[0] <= date.date() <= i.date_interval[1]:
                return i.schedule
        return []

    def _fit_time(self, thetime):
        if self.begin_time is None or self.end_time is None:
            return True
        return self.begin_time <= thetime.time() <= self.end_time

    def _fit_date(self, thetime):
        if self.begin_date is None or self.end_date is None:
            return True
        return self.begin_date <= thetime.date() <= self.end_date

    def __str__(self):
        return self.filename

    def __repr__(self):
        return self.__str__()


class ScheduleInterval(object):
    def __init__(self, raw_dict):
        self._raw_dict = raw_dict

    @property
    def date_interval(self):
        return parse_date(self._raw_dict['date_interval']['begin']), parse_date(self._raw_dict['date_interval']['end'])

    @property
    def schedule(self):
        return [parse_time(i) for i in self._raw_dict['schedule']]
