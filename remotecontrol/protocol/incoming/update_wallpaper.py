# -*- coding: utf-8 -*-

import logging
import os
import urllib.parse

import remotecontrol.protocol.incoming.base_command as base_command
import system.wallpaper as wallpaper
import remotecontrol.httpclient as httpclient
import utils.config as config

log = logging.getLogger(__name__)


class UpdateWallpaper(base_command.BaseCommand):
    def call(self):
        url = self._data['url']
        localpath = wallpaper.Wallpaper().custom_image_path()
        log.info('downloading new wallpaper to {}'.format(localpath))
        self._download_file(url, localpath)
        ok = wallpaper.Wallpaper().load()
        return self._ack(ok)

    def _ack(self, ok):
        return self._sender('ack_' + ('ok' if ok else 'fail')).call(sequence=self._sequence, message='set wallpaper')

    def _download_file(self, url, localpath):
        if os.path.isfile(localpath):
            os.remove(localpath)
        httpclient.download_file(self._full_file_url(url), localpath)

    def _full_file_url(self, relativeurl):
        return urllib.parse.urljoin(config.Config().server_url(), relativeurl)

