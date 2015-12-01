# -*- coding: utf-8 -*-

import datetime


def now(timezone=None):
    return datetime.datetime.now(timezone)


def utcnow():
    return datetime.datetime.utcnow()
