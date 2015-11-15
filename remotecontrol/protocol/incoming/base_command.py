# -*- coding: utf-8 -*-

import remotecontrol.protocol.sender as sender


class BaseCommand(object):
    def __init__(self, control_wrapper, data, sequence):
        self._control_wrapper = control_wrapper
        self._data = data
        self._sequence = sequence

    def _sender(self, msgtype):
        return sender.Sender(self._control_wrapper, msgtype)


