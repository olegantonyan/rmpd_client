# -*- coding: utf-8 -*-

import logging
import threading
import time

import utils.singleton
import utils.threads
import utils.datetime
import mediaplayer.player.watcher as player

log = logging.getLogger(__name__)


class Scheduler(object, metaclass=utils.singleton.Singleton):
    lock = threading.RLock()

    def __init__(self):
        self._player = player.Watcher()
        self._playlist = None
        self._player.set_callbacks(onfinished=self._onfinished)
        self._thread = threading.Thread(target=self._loop)
        self._thread.setDaemon(True)
        self._stop_flag = False
        self._thread.start()
        self._now_playing = None

    @utils.threads.synchronized(lock)
    def set_playlist(self, playlist):
        log.info("start playlist")
        self._playlist = playlist
        self._play(self._playlist.current())

    @utils.threads.synchronized(lock)
    def _onfinished(self, **kwargs):
        log.debug("track finished {f}".format(f=kwargs.get('filepath', '')))
        self._play(self._playlist.next())

    def _play(self, item):
        if item is None:
            return False
        if self._player.play(item.filepath):
            self._set_now_playing(item)
            return True
        else:
            return False

    @utils.threads.synchronized(lock)
    def _set_now_playing(self, item):
        self._now_playing = item

    @utils.threads.synchronized(lock)
    def _get_now_playing(self):
        return self._now_playing

    def _loop(self):
        while not self._stop_flag:
            time.sleep(2)

    def __del__(self):
        self._stop_flag = True
