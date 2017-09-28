# -*- coding: utf-8 -*-

import os
import urllib.parse
import getpass

import utils.config as config
import utils.shell as shell
import hardware


def mediafiles_path():
    return config.Config().mediafiles_path()


def full_file_localpath(relative_url):
    file_path = mediafiles_path()
    full_path = os.path.join(file_path, os.path.basename(relative_url))
    return full_path


def full_url_by_relative(relativeurl):
    return urllib.parse.urljoin(config.Config().server_url(), relativeurl)


def mkdir(path):
    if hardware.platfrom.__name__ == 'raspberry':
        sudo = 'sudo '
    else:
        sudo = ''
    shell.execute("{s}mkdir -p {p}".format(p=path, s=sudo))
    chown_to_current(path)


def chmod(path, mode):
    shell.execute("sudo chmod -R {m} {p}".format(p=path, m=mode))


def chown(path, user, group):
    if hardware.platfrom.__name__ == 'raspberry':
        shell.execute("sudo chown -R {u}:{g} {p}".format(p=path, u=user, g=group))


def chown_to_current(path):
    chown(path, getpass.getuser(), os.getegid())
