# -*- coding: utf-8 -*-

import json
import threading
import logging
import traceback

import mediaplayer.playlist.playlist as playlist
import mediaplayer.playlist.loader as loader
import remotecontrol.protocol.incoming.base_command as base_command

log = logging.getLogger(__name__)


class BasePlaylistCommand(base_command.BaseCommand):
    def _save_playlist_file(self):
        playlst = self._data.get('playlist')
        if playlst is None:  # old server without 'playlist' key
            return
        localpath = self._playlist_file_path()
        jsondata = json.dumps(playlst)
        with open(localpath, 'w') as f:
            f.write(jsondata)

    def _reset_playlist_position(self):
        return playlist.Playlist.reset_position()

    def _playlist_file_path(self):
        return loader.Loader().filepath()


class BaseWorker(threading.Thread):
    def __init__(self, sequence, onfinish_callback):
        super().__init__()
        self._sequence = sequence
        self.daemon = True
        self._onfinish = onfinish_callback
        self._playlist_fullpath = loader.Loader().filepath()
        self._error_message = 'please set error message in subclass'
        self._success_message = 'please set verify message in subclass'
        self._terminate = False

    def run(self):
        try:
            self._run()
            log.info(self._success_message)
            self._onfinish(True, self._sequence, self._success_message)
        except WorkerTerminated:
            log.warn('terminated')
        except:
            log.error("{msg}\n{ex}".format(msg=self._error_message, ex=traceback.format_exc()))
            self._onfinish(False, self._sequence, self._error_message)

    def terminate(self):
        self._terminate = True

    def _check_terminate(self):
        if self._terminate:
            raise WorkerTerminated

    def _run(self):
        raise NotImplementedError('override this method in subclass')


class WorkerTerminated(RuntimeError):
    pass
