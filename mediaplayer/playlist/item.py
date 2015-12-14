# -*- coding: utf-8 -*-

import datetime

import utils.files
import mediaplayer.playlist.schedule as sched


class Item(object):
    def __init__(self, i):
        self._d = i
        if self.is_advertising:
            self.schedule = sched.Schedule(self.begin_time, self.end_time, self.playbacks_per_day)
        else:
            self.schedule = None

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

    def next_play_time(self, thetime):
        if self.is_background or self.schedule is None:
            return None
        return self.schedule.next_play_time(thetime)

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
        return datetime.datetime.strptime(arg, '%d.%m.%Y').date()
