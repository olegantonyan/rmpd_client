# -*- coding: utf-8 -*-

import threading
import logging
import os

import remotecontrol.protocol.incoming.base_playlist_command as base_playlist_command
import mediaplayer.playercontroller as playercontroller
import utils.files as files
import mediaplayer.playlist.loader as loader


log = logging.getLogger(__name__)


class DeletePlaylist(base_playlist_command.BasePlaylistCommand):
    worker = None
    lock = threading.Lock()

    @staticmethod
    def busy():
        return DeletePlaylist.worker is not None

    def call(self):
        if self.__class__.busy():
            log.warning("trying to start delete worker while another one is active")
            return
        return self._start_worker()

    def _onfinish(self, ok, sequence, message):
        self._release_worker()
        if ok:
            self._reset_playlist_position()
            playercontroller.PlayerController().stop()
        self._send_ack(ok, sequence, message)

    def _start_worker(self):
        self.__class__.lock.acquire()
        self.__class__.worker = Worker(self._sequence, self._onfinish)
        self.__class__.lock.release()
        return self.__class__.worker.start()

    def _release_worker(self):
        self.__class__.lock.acquire()
        self.__class__.worker = None
        self.__class__.lock.release()


class Worker(base_playlist_command.BaseWorker):
    def __init__(self, sequence, onfinish_callback):
        base_playlist_command.BaseWorker.__init__(self, sequence, onfinish_callback)
        self._error_message = 'error deleting playlist'
        self._success_message = 'playlist deleted successfully'

    def _run(self):
        for f in loader.Loader(self._playlist_fullpath).list_all_files():
            self._remove_file(files.full_file_localpath(f))
        self._remove_file(self._playlist_fullpath)

    def _remove_file(self, file):
        try:
            os.remove(file)
        except FileNotFoundError:
            pass
