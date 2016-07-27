# -*- coding: utf-8 -*-

import os
import urllib.parse

import utils.config as config


def mediafiles_path():
    return config.Config().mediafiles_path()


def full_file_localpath(relative_url):
    file_path = mediafiles_path()
    full_path = os.path.join(file_path, os.path.basename(relative_url))
    return full_path


def full_url_by_relative(relativeurl):
    return urllib.parse.urljoin(config.Config().server_url(), relativeurl)
