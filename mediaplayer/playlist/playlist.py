# -*- coding: utf-8 -*-

import random

import mediaplayer.playlist.loader as loader
import mediaplayer.playlist.item as playlist_item
import utils.files
import utils.datetime


class Playlist(object):
    def __init__(self):
        self._data = loader.Loader().load()
        self._background = self._background_items()
        self._advertising = self._advertising_items()
        self._current_background_position = 0

    @staticmethod
    def reset_position():
        pass

    def next_background(self):
        next_item, index = self._find_next_appropriate(self._background,
                                                       self._current_background_position + 1,
                                                       len(self._background))
        if next_item is not None:
            return next_item
        next_item, index = self._find_next_appropriate(self._background,
                                                       0,
                                                       self._current_background_position + 1)
        if next_item is not None:
            return next_item
        return None

    def fisrt_background(self):  # start playlist from this item
        next_item, index = self._find_next_appropriate(self._background,
                                                       0,
                                                       len(self._background))
        return next_item

    def next_advertising(self):
        thetime = self._thetime()
        appropriate_now = [i for i in self._advertising if i.is_appropriate_at(thetime)]
        if len(appropriate_now) == 0:
            return None
        for i in appropriate_now:
            if i.is_required_at(thetime):
                return i
        return None

    def onfinished(self, item):
        if item is None:
            return
        if item.is_advertising:
            pass
        elif item.is_background:
            self._current_background_position = self._background_item_position(item)

    def _find_next_appropriate(self, collection, start_pos, end_pos):
        thetime = self._thetime()
        if len(collection) == 1:
            if collection[0].is_appropriate_at(thetime):
                return collection[0], 0
            else:
                return None, None
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
