# -*- coding: utf-8 -*-

import datetime
import tzlocal


def now(timezone=tzlocal.get_localzone()):
    return datetime.datetime.now(timezone)


def utcnow():
    return datetime.datetime.utcnow()
