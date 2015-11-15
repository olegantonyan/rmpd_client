# -*- coding: utf-8 -*-

import threading
import logging
import os
import urllib
import traceback

import utils.files
import utils.state
import remotecontrol.protocol.incoming.base_command
import system.status
import remotecontrol.httpclient
import mediaplayer.playercontroller

log = logging.getLogger(__name__)


class UpdatePlaylist(remotecontrol.protocol.incoming.base_command.BaseCommand):
    worker = None
    lock = threading.Lock()

    @staticmethod
    def busy():
        return UpdatePlaylist.worker is not None

    def call(self):
        if self.__class__.busy():
            log.warning("trying to start update worker while another one is active")
            return
        # playlist = self._data['playlist']
        legacy_items = self._data['items']
        self._sender('update_playlist').call(files=[os.path.basename(i) for i in legacy_items])
        system.status.Status().downloading = True
        return self._start_worker(legacy_items)

    def _onfinish(self, ok, sequence, message):
        self._release_worker()
        system.status.Status().downloading = False
        if ok:
            utils.state.State().current_track_num = 0
            mediaplayer.playercontroller.PlayerController().start_playlist()
        self._sender('ack').call(ok=ok, sequence=sequence, message=message)

    def _start_worker(self, legacy_items):
        self.__class__.lock.acquire()
        self.__class__.worker = Worker(legacy_items, self._sequence, self._onfinish)
        self.__class__.lock.release()
        return self.__class__.worker.start()

    def _release_worker(self):
        self.__class__.lock.acquire()
        self.__class__.worker = None
        self.__class__.lock.release()


class Worker(threading.Thread):
    def __init__(self, media_items, seq, onfinish_callback):
        threading.Thread.__init__(self)
        self.__media_items = media_items
        self.__seq = seq
        self.daemon = True
        self._onfinish = onfinish_callback

    def run(self):
        try:
            for i in self.__media_items:
                if i is not None:
                    self._download_file(i)
            self._utilize_nonplaylist_files(self.__media_items, utils.files.mediafiles_path())
            self._onfinish(True, self.__seq, "playlist updated successfully")
        except Exception:
            log.error("error updating playlist\n{ex}".format(ex=traceback.format_exc()))
            self._onfinish(False, self.__seq, "playlist update error")

    def _download_file(self, file):
        url = self._full_file_url(file)
        localpath = utils.files.full_file_localpath(file)
        if not os.path.isfile(localpath) or localpath.endswith("m3u"):
            log.info("downloading file '%s'", url)
            remotecontrol.httpclient.download_file(url, localpath)

    def _full_file_url(self, relativeurl):
        return urllib.parse.urljoin(utils.config.Config().server_url(), relativeurl)

    def _utilize_nonplaylist_files(self, media_items, media_items_path):
        media_items = [os.path.basename(i) for i in media_items]
        for file in os.listdir(media_items_path):
            if file not in media_items and not file.endswith('.log'):
                log.info("removing file not in current playlist '{f}'".format(f=file))
                os.remove(utils.files.full_file_localpath(file))
