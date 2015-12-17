# -*- coding: utf-8 -*-

import datetime
import tzlocal


def now(timezone=tzlocal.get_localzone()):
    return datetime.datetime.now(timezone)


def utcnow():
    return datetime.datetime.utcnow()


def time_to_seconds(tm):
    return tm.hour * 3600 + tm.minute * 60 + tm.second


def time_from_seconds(secs):
    h = int(secs / 3600)
    rem = (secs % 3600)
    m = int(rem / 60)
    s = int(rem % 60)
    return datetime.time(hour=h, minute=m, second=s)


def time_to_string(tm):
    return '{h:02d}:{m:02d}:{s:02d}'.format(h=tm.hour, m=tm.minute, s=tm.second)


def datetime_from_time(tm, thetime=now()):
        dt = datetime.datetime(year=thetime.year,
                               month=thetime.month,
                               day=thetime.day,
                               hour=tm.hour,
                               minute=tm.minute,
                               second=tm.second,
                               tzinfo=thetime.tzinfo)
        return dt
