#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from configparser import SafeConfigParser
from os import path, remove
from codecs import open

import utils.singleton  # @UnusedImport

class State(object, metaclass=utils.singleton.Singleton):
    '''
    Handles state data
    '''

    def __init__(self, filename):
        self.__parser = SafeConfigParser()
        self.__filename = filename
        for i in range(3): # re-create corrupted file
            self.__create_file_if_needed()
            try:
                self.__read_file()
                break
            except Exception as e:
                remove(self.__filename)

    @property
    def current_track_num(self):
        return self.__current_track_num

    @current_track_num.setter
    def current_track_num(self, num):
        with open(self.__filename, 'w', encoding='utf-8') as f:
            self.__parser.set('playlist', 'current_track_num', str(num))
            self.__parser.write(f)
        self.__current_track_num = num

    def __create_file_if_needed(self):
        if not path.exists(self.__filename):
            with open(self.__filename, 'w', encoding='utf-8') as f:
                self.__parser = SafeConfigParser()
                self.__parser.add_section('playlist')
                self.__parser.set('playlist', 'current_track_num', '0')
                self.__parser.write(f)

    def __read_file(self):
        with open(self.__filename, 'r', encoding='utf-8') as f:
            self.__parser.readfp(f)

        section = 'playlist'
        self.__current_track_num = int(self.__parser.get(section, 'current_track_num'))
