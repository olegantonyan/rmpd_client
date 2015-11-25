# -*- coding: utf-8 -*-

import utils.state
import utils.files

import json


class Playlist(object):
    def __init__(self):
        self._loader = PlaylistLoader()
        self._filepath = self._loader.filepath()
        self._data = self._loader.load()
        self._list = self._loader.list_all_files()
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


class PlaylistLoader(object):
    def __init__(self, filename='playlist.json'):
        self._filename = filename
        self._filepath = utils.files.full_file_localpath(self._filename)

    def filepath(self):
        return self._filepath

    def list_all_files(self):
        return [i['filename'] for i in self.load()['items']]

    def load(self):
        with open(self.filepath(), 'r') as file:
            return json.load(file)
