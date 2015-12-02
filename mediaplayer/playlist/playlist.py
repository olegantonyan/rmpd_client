# -*- coding: utf-8 -*-

import utils.state
import utils.files
import utils.datetime
import random

import mediaplayer.playlist.loader
import mediaplayer.playlist.item as item


class Playlist(object):
    def __init__(self):
        self._loader = mediaplayer.playlist.loader.Loader()
        self._data = self._loader.load()
        self._list = self._loader.list_all_files()
        self._items = self._fill_items()
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

    def _thetime(self):
        return utils.datetime.now().time()

    def _fill_items(self):
        raw_items = [item.Item(i) for i in self._data['items']]
        if self._data['shuffle']:
            random.shuffle(raw_items)
            return raw_items
        else:
            return sorted(raw_items, key=lambda j: j.position)


