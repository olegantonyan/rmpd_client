# -*- coding: utf-8 -*-

import logging
import os
import time
import threading

import utils.smart_queue as smart_queue
import utils.config as config
import utils.threads as threads
import system.rw_fs as rw_fs

log = logging.getLogger(__name__)


class MessageQueue(object):
    def __init__(self):
        db_params = {'path': os.path.join(config.Config().storage_path(), 'message_queue.db'),
                     'table': 'message_queue'}

        self._queue = smart_queue.SmartQueue(maxlen=200000, db_params=db_params)
        self._start_sync_timer()
        self._wait_condition = threading.Condition()

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

    def _player(self):
        import mediaplayer.playercontroller as playercontroller
        return playercontroller.PlayerController()

    def _start_sync_timer(self):
        sync_period = config.Config().message_queue_sync_period() * 3600
        if sync_period == 0:
            return
        threads.run_after_timeout(sync_period, self._on_sync_period)

    def _on_sync_period(self):
        log.info('about time to run message queue sync')
        player = self._player()
        try:
            if player.isplaying():
                log.info('waiting for player to finish')
                player.set_scheduler_callback('on_before_play', self._run_sync)
                self._wait_for_sync_to_complete()
            else:
                player.set_scheduler_callback('on_before_play', self._wait_for_sync_to_complete)
                self._run_sync()
        finally:
            log.info('message queue sync finished')
            player.set_scheduler_callback('on_before_play', None)
            self._start_sync_timer()

    def _run_sync(self, *args):
        try:
            log.info('running message queue sync')
            with rw_fs.Storage(restart_player=False):
                self._queue.sync()
        except:
            log.exception('error running message queue sync')
        finally:
            with self._wait_condition:
                self._wait_condition.notify_all()

    def _wait_for_sync_to_complete(self, *args):
        with self._wait_condition:
            self._wait_condition.wait()
