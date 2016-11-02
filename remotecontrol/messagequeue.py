# -*- coding: utf-8 -*-

import logging
import os

import utils.datetime as datetime
import utils.smart_queue as smart_queue

log = logging.getLogger(__name__)


class MessageQueue(object):
    def __init__(self):
        self._queue = smart_queue.SmartQueue(maxlen=100000)

    def enqueue(self, data):
        self._queue.enqueue({'data': data, 'created_at': datetime.utcnow(), 'id': 0})

    def dequeue(self):
        try:
            data = self._queue.peek()
            return data['id'], data['data']
        except IndexError:
            return None, None

    def remove(self, messageid):
        try:
            self._queue.dequeue()
        except IndexError:
            return None

