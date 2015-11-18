# -*- coding: utf-8 -*-

import json
import os

import utils.files
import remotecontrol.protocol.incoming.base_command


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