# -*- coding: utf-8 -*-

import threading
import logging
import os
import urllib
import traceback

import utils
import remotecontrol

log = logging.getLogger(__name__)


class UpdatePlaylist(remotecontrol.protocol.incoming.base_command.BaseCommand):
    def call(self):
        # TODO send notification
        playlist = self._data['playlist']


class UpdateWorker(threading.Thread):
    def __init__(self, media_items, seq, onfinish_callback):
        # threading.Thread.__init__(self)
        super()
        self.__media_items = media_items
        self.__seq = seq
        self.daemon = True
        self._onfinish = onfinish_callback

    def run(self):
        try:
            for i in self.__media_items:
                if i is not None:
                    self._download_file(i)
            utils.state.State().current_track_num = 0
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
