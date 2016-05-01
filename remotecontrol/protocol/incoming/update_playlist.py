# -*- coding: utf-8 -*-

import threading
import logging
import os
import urllib.parse

import utils.files as files
import utils.config as config
import utils.support as support
import remotecontrol.protocol.incoming.base_playlist_command as base_playlist_command
import system.status as status
import remotecontrol.httpclient as httpclient
import mediaplayer.playercontroller as playercontroller

log = logging.getLogger(__name__)


class UpdatePlaylist(base_playlist_command.BasePlaylistCommand):
    worker = None
    lock = threading.Lock()

    @staticmethod
    def busy():
        return UpdatePlaylist.worker is not None

    def call(self):
        if self.__class__.busy():
            log.warning("trying to start update worker while another one is active")
            return
        media_items = self._media_items()
        self._sender('update_playlist').call(files=[os.path.basename(i) for i in media_items])
        status.Status().downloading = True
        return self._start_worker(media_items)

    def _onfinish(self, ok, sequence, message):
        self._release_worker()
        status.Status().downloading = False
        if ok:
            self._save_playlist_file()  # successfully downloaded => save new playlist file
            self._reset_playlist_position()
            playercontroller.PlayerController().start_playlist()
        self._send_ack(ok, sequence, message)

    def _start_worker(self, legacy_items):
        self.__class__.lock.acquire()
        self.__class__.worker = Worker(legacy_items, self._sequence, self._onfinish)
        self.__class__.lock.release()
        return self.__class__.worker.start()

    def _release_worker(self):
        self.__class__.lock.acquire()
        self.__class__.worker = None
        self.__class__.lock.release()

    def _media_items(self):
        return [i['url'] for i in self._data['playlist']['items']]


class Worker(base_playlist_command.BaseWorker):
    def __init__(self, media_items, sequence, onfinish_callback):
        base_playlist_command.BaseWorker.__init__(self, sequence, onfinish_callback)
        self._media_items = support.list_compact(media_items)
        self._error_message = 'error updating playlist'
        self._success_message = 'playlist updated successfully'

    def _run(self):
        for i in self._media_items:
            self._download_file(i)
        self._utilize_nonplaylist_files(self._media_items, files.mediafiles_path())

    def _download_file(self, file):
        url = self._full_file_url(file)
        localpath = files.full_file_localpath(file)
        if not os.path.isfile(localpath):
            log.info("downloading file '%s'", url)
            httpclient.download_file(url, localpath)

    def _full_file_url(self, relativeurl):
        return urllib.parse.urljoin(config.Config().server_url(), relativeurl)

    def _utilize_nonplaylist_files(self, media_items, media_items_path):
        media_items = [os.path.basename(i) for i in media_items]
        for file in os.listdir(media_items_path):
            if file not in media_items \
                    and not file.endswith('.log') \
                    and not file.endswith(os.path.basename(self._playlist_fullpath)):
                log.info("removing file not in current playlist '{f}'".format(f=file))
                os.remove(files.full_file_localpath(file))
