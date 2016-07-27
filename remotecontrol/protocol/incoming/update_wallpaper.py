# -*- coding: utf-8 -*-

import logging
import os
import threading

import remotecontrol.protocol.incoming.base_command as base_command
import system.wallpaper as wallpaper
import remotecontrol.httpclient as httpclient
import utils.files as files

log = logging.getLogger(__name__)


class UpdateWallpaper(base_command.BaseCommand):
    def call(self):
        url = self._data['url']
        return Worker(url, self._sequence, self._onfinish).start()

    def _onfinish(self, ok, sequence):
        if ok:
            ok = wallpaper.Wallpaper().load()
        return self._sender('ack_' + ('ok' if ok else 'fail')).call(sequence=sequence, message='set wallpaper')


class Worker(threading.Thread):
    def __init__(self, url, sequence, onfinish_callback):
        threading.Thread.__init__(self)
        self._onfinish = onfinish_callback
        self._sequence = sequence
        self._url = url

    def run(self):
        try:
            localpath = wallpaper.Wallpaper().custom_image_path()
            if self._url is not None:
                log.info('downloading new wallpaper to {}'.format(localpath))
                self._download_file(self._url, localpath)
            else:
                self._remove_file(localpath)
            self._onfinish(True, self._sequence)
        except:
            log.exception('error downloading wallpaper')
            self._onfinish(False, self._sequence)

    def _download_file(self, url, localpath):
        if os.path.isfile(localpath):
            os.remove(localpath)
        httpclient.download_file(files.full_url_by_relative(url), localpath)

    def _remove_file(self, file):
        try:
            os.remove(file)
        except FileNotFoundError:
            pass
