# -*- coding: utf-8 -*-

import threading
import traceback
import logging
import os

import remotecontrol.protocol.incoming.base_playlist_command
import mediaplayer.playercontroller
import utils.files

log = logging.getLogger(__name__)


class DeletePlaylist(remotecontrol.protocol.incoming.base_playlist_command.BasePlaylistCommand):
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
            self._remove_playlist_file()
            mediaplayer.playercontroller.PlayerController().stop()
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


class Worker(threading.Thread):
    def __init__(self, sequence, onfinish_callback):
        threading.Thread.__init__(self)
        self._sequence = sequence
        self.daemon = True
        self._onfinish = onfinish_callback

    def run(self):
        try:
            playlist_fullpath = utils.files.full_file_localpath("playlist.m3u")
            for f in utils.files.list_files_in_playlist(playlist_fullpath):
                self._remove_mediaifile(f)
            os.remove(playlist_fullpath)
            utils.state.State().current_track_num = 0
            self._onfinish(True, self._sequence, "playlist deleted successfully")
        except Exception:
            log.error("error deleting playlist\n{ex}".format(ex=traceback.format_exc()))
            self._onfinish(False, self._sequence, "playlist delete error")

    def _remove_mediaifile(self, file):
        try:
            os.remove(utils.files.full_file_localpath(file))
        except FileNotFoundError:
            pass
