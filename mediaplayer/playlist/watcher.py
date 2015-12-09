# -*- coding: utf-8 -*-

import logging
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
        log.info("start playlist")
        self._playlist = playlist
        self._player.play(self._playlist.current().filepath)

    @utils.threads.synchronized(lock)
    def _onfinished(self, **kwargs):
        log.debug("track finished")
        self._player.play(self._playlist.next().filepath)
