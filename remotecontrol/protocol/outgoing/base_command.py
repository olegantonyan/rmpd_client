# -*- coding: utf-8 -*-

import utils.support
import utils.datetime


class BaseCommand(object):
    def __init__(self, control_wrapper):
        self._control_wrapper = control_wrapper
        self._queued = True   # override in subclass
        self._sequence = 0    # // - //
        self._message = None  # // - //
        self._json = {}       # // - //

    def call(self):
        return self._send()

    def _thetime(self):
        return utils.datetime.now().strftime('%Y-%m-%dT%H:%M:%S%z')

    def _send(self):
        full_json = dict(self._json, **{'localtime': self._thetime(), 'command': self._type(), 'message': self._message})
        return self._control_wrapper.send(full_json, self._queued, self._sequence)

    def _type(self):
        return utils.support.camelcase_to_underscore(self.__class__.__name__)
