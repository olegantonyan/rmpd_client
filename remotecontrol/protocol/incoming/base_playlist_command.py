# -*- coding: utf-8 -*-

import json
import threading
import logging
import traceback

import mediaplayer.playlist.playlist as p
import mediaplayer.playlist.loader as pl
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

    def _reset_playlist_position(self):
        return p.Playlist.reset_position()

    def _playlist_file_path(self):
        return pl.Loader().filepath()

    def _send_ack(self, ok, sequence, message):
        self._sender('ack_' + ('ok' if ok else 'fail')).call(sequence=sequence, message=message)


class BaseWorker(threading.Thread):
    def __init__(self, sequence, onfinish_callback):
        threading.Thread.__init__(self)
        self._sequence = sequence
        self.daemon = True
        self._onfinish = onfinish_callback
        self._playlist_fullpath = pl.Loader().filepath()
        self._error_message = 'please set error message in subclass'
        self._success_message = 'please set success message in subclass'

    def run(self):
        try:
            self._run()
            log.info(self._success_message)
            self._onfinish(True, self._sequence, self._success_message)
        except:
            log.error("{msg}\n{ex}".format(msg=self._error_message, ex=traceback.format_exc()))
            self._onfinish(False, self._sequence, self._error_message)

    def _run(self):
        raise NotImplementedError('override this method in subclass')

