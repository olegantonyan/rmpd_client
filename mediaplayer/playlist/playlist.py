# -*- coding: utf-8 -*-

import random
import datetime

import mediaplayer.playlist.loader as loader
import mediaplayer.playlist.item as playlist_item
import mediaplayer.player.state as state
import utils.state
import utils.files
import utils.datetime


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
        state.State().reset()

    def save_position(self):
        pass  # utils.state.State().current_track_num = self._current_position

    def next_background(self):
        next_item, index = self._find_next_appropriate(self._background,
                                                       self._current_background_position + 1,
                                                       len(self._background))
        if next_item is not None:
            return next_item
        next_item, index = self._find_next_appropriate(self._background,
                                                       0,
                                                       self._current_background_position)
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
        thetime = self._thetime()
        appropriate_now = [i for i in self._advertising if i.is_appropriate_at(thetime)]
        if len(appropriate_now) == 0:
            return None
        for i in appropriate_now:
            period = i.period_in_seconds
            played_today = self._state.fetch_playbacks_count(i.id, thetime)
            begin_time = i.begin_time
            dt = datetime.datetime(year=thetime.year,
                                   month=thetime.month,
                                   day=thetime.day,
                                   hour=begin_time.hour,
                                   minute=begin_time.minute,
                                   second=begin_time.second,
                                   tzinfo=thetime.tzinfo)
            next_play_time = dt + datetime.timedelta(seconds=(period * played_today))
            print("******")
            print(i.filename)
            print(next_play_time)
            print("******")
            if thetime >= next_play_time:
                return i

    def playbacks_remain_today(self, item):
        return item.playbacks_per_day - self._state.fetch_playbacks_count(item.id, self._thetime())

    def onfinished(self, item):
        if item is None:
            return
        if item.is_advertising:
            self._state.increment_playbacks_count(item.id, self._thetime())
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
