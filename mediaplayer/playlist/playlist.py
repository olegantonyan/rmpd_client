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
        self._background = self._background_items()
        self._advertising = self._advertising_items()
        self._current_position = 0  # utils.state.State().current_track_num
        if self._current_position >= len(self._background):
            self._current_position = 0
            self.save_position()

    @staticmethod
    def reset_position():
        pass  # utils.state.State().current_track_num = 0

    def save_position(self):
        pass  # utils.state.State().current_track_num = self._current_position

    def next(self):
        self._current_position += 1
        if self._current_position % len(self._background) == 0:
            self._current_position = 0
        return self.current()

    def current(self):
        return self._background[self._current_position]

    def _thetime(self):
        return utils.datetime.now().time()

    def _background_items(self):
        raw_items = list(filter(lambda i: i.is_background, self._all_items()))
        if self._data['shuffle']:
            random.shuffle(raw_items)
            return raw_items
        else:
            return sorted(raw_items, key=lambda j: j.position)

    def _advertising_items(self):
        return list(filter(lambda i: i.is_advertising, self._all_items()))

    def _all_items(self):
        return [item.Item(i) for i in self._data['items']]



