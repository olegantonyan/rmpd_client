# -*- coding: utf-8 -*-

import datetime
import tzlocal

import utils.support

class BaseCommand(object):
    def __init__(self, control_wrapper):
        self._control_wrapper = control_wrapper
        self._queued = True  # override in subclass
        self._sequence = 0   # // - //

    def _thetime(self):
        return datetime.datetime.now(tzlocal.get_localzone()).strftime("%Y-%m-%dT%H:%M:%S%z")

    def _send(self, json):
        full_json = dict(json, **{'localtime': self._thetime(), 'command': self._type()})
        return self._control_wrapper.send(full_json, self._queued, self._sequence)

    def _type(self):
        return utils.support.camelcase_to_underscore(self.__class__.__name__)

