# -*- coding: utf-8 -*-

import logging
import os
import threading

import utils.singleton
import utils.threads
import mediaplayer.player.watcher as player

log = logging.getLogger(__name__)


class Watcher(object, metaclass=utils.singleton.Singleton):
    lock = threading.Lock()

    def __init__(self):
        self._player = player.Watcher()
        self._playlist = None
        self._player.set_callbacks(onfinished=self._onfinished)

    @utils.threads.synchronized(lock)
    def set_playlist(self, playlist):
        self._playlist = playlist

    @utils.threads.synchronized(lock)
    def _onfinished(self, **kwargs):
        print("finished")
        self._player.play(self._playlist.next())
