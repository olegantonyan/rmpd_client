# -*- coding: utf-8 -*-

import utils.state
import utils.files


class Playlist(object):
    def __init__(self, playlist_file):
        self._playlistfile = utils.files.full_file_localpath(playlist_file)
        self._list = utils.files.list_files_in_playlist(self._playlistfile)
        self._current_position = utils.state.State().current_track_num
        if self._current_position >= len(self._list):
            self._current_position = 0
            self.save_position()

    def save_position(self):
        utils.state.State().current_track_num = self._current_position

    def reset_position(self):
        utils.state.State().current_track_num = 0

    def next(self):
        self._current_position += 1
        if self._current_position % len(self._list) == 0:
            self._current_position = 0
        return self.current()

    def pick_prev(self):
        prev_position = self._current_position - 1
        if prev_position < 0:
            prev_position = len(self._list) - 1
        return utils.files.full_file_localpath(self._list[prev_position])

    def current(self):
        return utils.files.full_file_localpath(self._list[self._current_position])
