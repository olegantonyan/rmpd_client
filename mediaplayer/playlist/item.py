# -*- coding: utf-8 -*-


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
        return self._d['begin_time']

    @property
    def end_time(self):
        return self._d['end_time']

    @property
    def begin_date(self):
        return self._d['begin_date']

    @property
    def end_date(self):
        return self._d['end_date']

    @property
    def playbacks_per_day(self):
        return self._d['playbacks_per_day']

    def is_background(self):
        return self.type == 'background'

    def is_advertising(self):
        return self.type == 'advertising'
