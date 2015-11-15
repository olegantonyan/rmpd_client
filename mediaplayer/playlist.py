# -*- coding: utf-8 -*-

import utils.state
import utils.files


class Playlist(object):
    def __init__(self, playlist_file):
        self.__playlistfile = utils.files.full_file_localpath(playlist_file)
        self.__list = utils.files.list_files_in_playlist(self.__playlistfile)
        self.__current_position = utils.state.State().current_track_num
        if self.__current_position >= len(self.__list):
            self.__current_position = 0
            self.save_position()

    def save_position(self):
        utils.state.State().current_track_num = self.__current_position

    def reset_position(self):
        utils.state.State().current_track_num = 0

    def next(self):
        self.__current_position += 1
        if self.__current_position % len(self.__list) == 0:
            self.__current_position = 0
        return self.current()

    def pick_prev(self):
        prev_position = self.__current_position - 1
        if prev_position < 0:
            prev_position = len(self.__list) - 1
        return utils.files.full_file_localpath(self.__list[prev_position])

    def current(self):
        return utils.files.full_file_localpath(self.__list[self.__current_position])
