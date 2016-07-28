# -*- coding: utf-8 -*-

import logging
import os

import remotecontrol.protocol.incoming.base_command as base_command
import system.self_update as self_update
import utils.threads as threads
import remotecontrol.httpclient as httpclient
import utils.files as files

log = logging.getLogger(__name__)


class UpdateSoftware(base_command.BaseCommand):
    def call(self):
        url = self._data.get('distribution_url')
        full_url = files.full_url_by_relative(url)
        filename = os.path.basename(url)
        full_localpath = os.path.join('/tmp', filename)
        threads.run_in_thread(self._download, [full_url, full_localpath, self._sequence])

    def _download(self, url, localpath, seq):
        try:
            log.info('starting software update download from % to %s', url, localpath)
            if os.path.isfile(localpath):
                os.remove(localpath)
            httpclient.download_file(url, localpath)
            self_update.SelfUpdate().downloaded(localpath, seq)
        except:
            log.exception('error downloading software update')


