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
        self._now_playing = None
        self._player.set_callbacks(onfinished=self._onfinished)
        self._thread = threading.Thread(target=self._loop)
        self._thread.setDaemon(True)
        self._stop_flag = False
        self._thread.start()

    @utils.threads.synchronized(lock)
    def set_playlist(self, playlist):
        log.info("start playlist")
        self._playlist = playlist
        item_to_start = self._playlist.current_background()
        if item_to_start is None:
            self._stop()
        else:
            self._play(item_to_start)

    @utils.threads.synchronized(lock)
    def _onfinished(self, **kwargs):
        log.debug("track finished {f}".format(f=kwargs.get('filepath', '')))
        current = self._get_now_playing()
        if current is None:
            self._play_nex_background()
            return

        if current.is_background:
            self._play_nex_background()
        elif current.is_advertising:
            # find nex advertising. keep adv block
            # if found adv: play it else: next_background
            pass

    @utils.threads.synchronized(lock)
    def _play(self, item):
        if item is None:
            self._set_now_playing(None)
            return False
        self._player.play(item.filepath)
        self._set_now_playing(item)

    @utils.threads.synchronized(lock)
    def _stop(self):
        self._set_now_playing(None)
        self._player.stop()

    @utils.threads.synchronized(lock)
    def _play_nex_background(self):
        if self._playlist is not None:
            self._play(self._playlist.next_background())

    @utils.threads.synchronized(lock)
    def _set_now_playing(self, item):
        self._now_playing = item

    @utils.threads.synchronized(lock)
    def _get_now_playing(self):
        return self._now_playing

    def _loop(self):
        while not self._stop_flag:
            current = self._get_now_playing()
            if current is None:
                self._play_nex_background()
            time.sleep(3)

    def __del__(self):
        self._stop_flag = True
