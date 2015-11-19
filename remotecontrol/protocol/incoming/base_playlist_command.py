# -*- coding: utf-8 -*-

import json
import os
import threading
import logging
import traceback

import utils.files
import remotecontrol.protocol.incoming.base_command

log = logging.getLogger(__name__)


class BasePlaylistCommand(remotecontrol.protocol.incoming.base_command.BaseCommand):
    def _save_playlist_file(self):
        playlist = self._data.get('playlist')
        if playlist is None:  # old server without 'playlist' key
            return
        localpath = self._playlist_file_path()
        jsondata = json.dumps(playlist)
        with open(localpath, 'w') as f:
            f.write(jsondata)

    def _remove_playlist_file(self):
        localpath = self._playlist_file_path()
        if os.path.isfile(localpath):
            os.remove(localpath)

    def _playlist_file_path(self):
        return utils.files.full_file_localpath('playlist.json')

    def _send_ack(self, ok, sequence, message):
        self._sender('ack').call(ok=ok, sequence=sequence, message=message)


class BaseWorker(threading.Thread):
    def __init__(self, sequence, onfinish_callback):
        threading.Thread.__init__(self)
        self._sequence = sequence
        self.daemon = True
        self._onfinish = onfinish_callback
        self._error_message = ''
        self._success_message = ''

    def run(self):
        try:
            self._run()
            log.info(self._success_message)
            self._onfinish(True, self._sequence, self._success_message)
        except:
            log.error("{msg}\n{ex}".format(msg=self._error_message, ex=traceback.format_exc()))
            self._onfinish(False, self._sequence, self._error_message)

