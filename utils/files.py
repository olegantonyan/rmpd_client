# -*- coding: utf-8 -*-

import os
import json

import utils
import utils.config


def mediafiles_path():
    return utils.config.Config().mediafiles_path()


def full_file_localpath(relative_url):
    file_path = mediafiles_path()
    full_path = os.path.join(file_path, os.path.basename(relative_url))
    return full_path


def list_files_in_playlist(playlist_file):  #TODO advertising and other
    with open(playlist_file, 'r') as file:
        data = json.load(file)
    return [i['filename'] for i in data['items']]
