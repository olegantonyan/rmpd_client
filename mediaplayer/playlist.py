# -*- coding: utf-8 -*-

import utils.state
import utils.files


def filename():
    return 'playlist.json'


def full_filepath():
    return utils.files.full_file_localpath(filename())


class Playlist(object):
    def __init__(self):
        self._playlistfile = full_filepath()  # utils.files.full_file_localpath("playlist.m3u")
        self._list = utils.files.list_files_in_playlist(self._playlistfile)
        self._current_position = utils.state.State().current_track_num
        if self._current_position >= len(self._list):
            self._current_position = 0
            self.save_position()

    @staticmethod
    def reset_position():
        utils.state.State().current_track_num = 0

    def save_position(self):
        utils.state.State().current_track_num = self._current_position

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
