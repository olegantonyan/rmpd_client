# -*- coding: utf-8 -*-

import remotecontrol.protocol.sender as sender


class BaseCommand(object):
    def __init__(self, control_wrapper, data, sequence):
        self._control_wrapper = control_wrapper
        self._data = data
        self._sequence = sequence

    def _sender(self, msgtype):
        return sender.Sender(self._control_wrapper, msgtype)

    def _ack(self, ok, message, sequence=None):
        if sequence is None:
            sequence = self._sequence
        return self._sender('ack_' + ('ok' if ok else 'fail')).call(sequence=sequence, message=message)


