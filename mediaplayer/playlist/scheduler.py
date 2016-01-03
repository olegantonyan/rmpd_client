# -*- coding: utf-8 -*-

import logging
import threading
import queue

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
        self._now_playing = None
        self._rx = queue.Queue()
        self._player.set_callbacks(onfinished=self.onfinished)
        self._stop_flag = False
        utils.threads.run_in_thread(self._loop)

    @utils.threads.synchronized(lock)
    def set_playlist(self, playlist):
        log.info("start playlist")
        self._playlist = playlist
        self._play(self._playlist.current_background())
        self._schedule()

    @utils.threads.synchronized(lock)
    def onfinished(self, **kwargs):
        log.info("track finished {f}".format(f=kwargs.get('filepath', '')))
        current_track = self._get_now_playing()
        if self._playlist is not None:
            self._playlist.onfinished(current_track)
        self._set_now_playing(None)
        self._schedule()

    @utils.threads.synchronized(lock)
    def _play(self, item):
        if item is None:
            self._set_now_playing(None)
            self._player.stop()
            return False
        self._player.play(item.filepath)
        self._set_now_playing(item)

    @utils.threads.synchronized(lock)
    def _set_now_playing(self, item):
        self._now_playing = item

    @utils.threads.synchronized(lock)
    def _get_now_playing(self):
        return self._now_playing

    def _schedule(self, arg=None):
        self._rx.put(arg)

    def _loop(self):
        while not self._stop_flag:
            try:
                self._rx.get(block=True, timeout=1)
            except queue.Empty:
                pass
            if self._playlist is not None:
                self._scheduler()

    def _scheduler(self):
        current_track = self._get_now_playing()

        next_advertising = self._playlist.next_advertising()
        if next_advertising is not None:
            if current_track is None or current_track.is_background:
                self._play(next_advertising)
        else:
            next_background = self._playlist.next_background()
            if next_background is not None:
                if current_track is None:
                    self._play(next_background)

    def __del__(self):
        self._stop_flag = True

