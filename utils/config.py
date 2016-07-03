# -*- coding: utf-8 -*-

import configparser
import codecs
import os

import system.control
import utils.singleton as singleton


class ConfigFileNotSpecifiedError(RuntimeError):
    pass


def _guard_initialization(func):
    def wrap(self, *args):
        if self._parser is None or self._filename is None:
            raise ConfigFileNotSpecifiedError("you have to specify config file with 'set_configfile()' method")
        return func(self, *args)
    return wrap


class Config(object, metaclass=singleton.Singleton):
    def __init__(self):
        self._filename = None
        self._parser = None

    def set_configfile(self, filename):
        self._filename = filename
        self._parse()

    @_guard_initialization
    def server_url(self):
        return self._server_url

    @_guard_initialization
    def login(self):
        return self._login

    @_guard_initialization
    def password(self):
        return self._password

    @_guard_initialization
    def logfile(self):
        return self._logfile

    @_guard_initialization
    def mediafiles_path(self):
        return self._mediafiles_path

    @_guard_initialization
    def mplayer_executable(self):
        return self._mplayer_executable

    @_guard_initialization
    def omplayer_executable(self):
        return self._omplayer_executable

    @_guard_initialization
    def omplayer_arguments(self):
        return self._omplayer_arguments

    @_guard_initialization
    def verbose_logging(self):
        return self._boolean_attr(self._verbose)

    @_guard_initialization
    def webui_password(self):
        return self._webui_password

    @_guard_initialization
    def set_webui_password(self, value):
        self._save_value('webui', 'password', value)
        self._webui_password = value

    @_guard_initialization
    def enable_clockd(self):
        return self._boolean_attr(self._enable_clockd)

    @_guard_initialization
    def wallpaper_path(self):
        return self._wallpaper_path

    @_guard_initialization
    def _save_value(self, section, option, value):
        try:
            system.control.Control().remount_rootfs()
            self._parser.set(section, option, str(value))
            with codecs.open(self._filename, 'w', encoding='utf-8') as f:
                self._parser.write(f)
        finally:
            system.control.Control().remount_rootfs(False)

    def _boolean_attr(self, attr):
        return attr == 'yes' or attr == 'y' or attr == 'true'

    def _parse(self):
        self._parser = configparser.ConfigParser()
        with codecs.open(self._filename, 'r', encoding='utf-8') as f:
            self._parser.read_file(f)

        section = 'remote_control'
        self._server_url = self._parser.get(section, 'server_url')
        self._login = self._parser.get(section, 'login')
        self._password = self._parser.get(section, 'password')

        section = 'logging'
        self._logfile = self._parser.get(section, 'logfile')
        self._verbose = self._parser.get(section, 'verbose')

        section = 'player'
        self._mediafiles_path = self._parser.get(section, 'mediafiles_path')
        self._mplayer_executable = self._parser.get(section, 'mplayer_executable')
        self._omplayer_executable = self._parser.get(section, 'omxplayer_executable')
        self._omplayer_arguments = self._parser.get(section, 'omxplayer_arguments')
        self._wallpaper_path = self._parser.get(section, 'wallpaper_path', fallback=os.path.join(os.getcwd(), 'wallpaper'))

        section = 'webui'
        self._webui_password = self._parser.get(section, 'password')

        section = 'clockd'
        self._enable_clockd = self._parser.get(section, 'enable', fallback='no')

