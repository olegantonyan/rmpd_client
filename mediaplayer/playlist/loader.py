# -*- coding: utf-8 -*-

import json

import utils.files as files


class Loader(object):
    def __init__(self, filename='playlist.json'):
        self._filename = filename
        self._filepath = files.full_file_localpath(self._filename)

    def filepath(self):
        return self._filepath

    def list_all_files(self):
        return [i['filename'] for i in self.load()['items']]

    def load(self):
        with open(self.filepath(), 'r') as file:
            return json.load(file)
