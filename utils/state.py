# -*- coding: utf-8 -*-

import configparser
import os
import codecs


import utils.singleton


class State(object, metaclass=utils.singleton.Singleton):
    def __init__(self, filename):
        self._parser = configparser.ConfigParser()
        self._filename = filename
        self._current_track_num = 0
        for i in range(3):  # re-create corrupted file
            self._create_file_if_needed()
            try:
                self._read_file()
                break
            except:
                os.remove(self._filename)

    @property
    def current_track_num(self):
        return self._current_track_num

    @current_track_num.setter
    def current_track_num(self, num):
        with codecs.open(self._filename, 'w', encoding='utf-8') as f:
            self._parser.set('playlist', 'current_track_num', str(num))
            self._parser.write(f)
        self._current_track_num = num

    def _create_file_if_needed(self):
        if not os.path.exists(self._filename):
            with codecs.open(self._filename, 'w', encoding='utf-8') as f:
                self._parser = configparser.ConfigParser()
                self._parser.add_section('playlist')
                self._parser.set('playlist', 'current_track_num', '0')
                self._parser.write(f)

    def _read_file(self):
        with codecs.open(self._filename, 'r', encoding='utf-8') as f:
            self._parser.read_file(f)
        section = 'playlist'
        self._current_track_num = int(self._parser.get(section, 'current_track_num'))
