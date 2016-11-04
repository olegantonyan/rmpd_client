# -*- coding: utf-8 -*-

import logging
import os

import utils.smart_queue as smart_queue
import utils.config as config
import utils.threads as threads

log = logging.getLogger(__name__)


class MessageQueue(object):
    def __init__(self):
        db_params = {'path': os.path.join(config.Config().storage_path(), 'message_queue.db'),
                     'table': 'message_queue'}
        self._sync_period = config.Config().message_queue_sync_period() * 3600
        self._queue = smart_queue.SmartQueue(maxlen=200000, db_params=db_params)
        self._run_sync_timer()

    def enqueue(self, data):
        self._queue.enqueue(data)

    def peek(self):
        try:
            return self._queue.peek()
        except IndexError:
            return None

    def dequeue(self):
        try:
            return self._queue.dequeue()
        except IndexError:
            return None

    def _run_sync_timer(self):
        threads.run_after_timeout(self._sync_period, self._sync_period)

    def _on_sync_period(self):
        # self._queue.sync() only when stopped
        self._run_sync_timer()

