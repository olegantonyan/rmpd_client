# -*- coding: utf-8 -*-

import utils.state
import utils.files
import utils.datetime
import random

import mediaplayer.playlist.loader as loader
import mediaplayer.playlist.item as playlist_item
import mediaplayer.player.state as state


class Playlist(object):
    def __init__(self):
        self._state = state.State()
        self._data = loader.Loader().load()
        self._background = self._background_items()
        self._advertising = self._advertising_items()
        self._current_background_position = 0  # utils.state.State().current_track_num
        if self._current_background_position >= len(self._background):
            self._current_background_position = 0
            self.save_position()

    @staticmethod
    def reset_position():
        pass  # utils.state.State().current_track_num = 0

    def save_position(self):
        pass  # utils.state.State().current_track_num = self._current_position

    def next_background(self):
        next_item, index = self._find_next_appropriate(self._background, self._current_background_position + 1, len(self._background))
        if next_item is not None:
            return next_item
        next_item, index = self._find_next_appropriate(self._background, 0, self._current_background_position)
        if next_item is not None:
            return next_item
        return None

    def current_background(self):
        current_item = self._background[self._current_background_position]
        if current_item.is_appropriate_at(self._thetime()):
            return current_item
        else:
            return None

    def next_advertising(self):
        return None

    def playbacks_remain_today(self, item):
        return item.playbacks_per_day - self._state.fetch_playbacks_count(item.id, self._thetime())

    def onfinished(self, item):
        if item is None:
            return
        if item.is_advertising:
            self._state.increment_playbacks_count(item, self._thetime())
        elif item.is_background:
            self._current_background_position = self._background_item_position(item)

    def _find_next_appropriate(self, collection, start_pos, end_pos):
        thetime = self._thetime()
        for i in range(start_pos, end_pos):
            next_item = collection[i]
            if next_item.is_appropriate_at(thetime):
                return next_item, i
        return None, None

    def _background_item_position(self, itm):
        for index, i in enumerate(self._background):
            if i.id == itm.id:
                return index

    def _thetime(self):
        return utils.datetime.now()

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
        return [playlist_item.Item(i) for i in self._data['items']]
