# -*- coding: utf-8 -*-

import os

import utils
import utils.config


def mediafiles_path():
    return utils.config.Config().mediafiles_path()


def full_file_localpath(relative_url):
    file_path = mediafiles_path()
    full_path = os.path.join(file_path, os.path.basename(relative_url))
    return full_path

