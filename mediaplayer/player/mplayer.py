# -*- coding: utf-8 -*-

import mplayer

import utils.config


class MPlayer(object):
    SEEK_MODE_SECONDS_RELATIVE = 0
    SEEK_MODE_PERCENTS_ABSOLUTE = 1
    SEEK_MODE_SECONDS_ABSOLUTE = 2

    def __init__(self):
        mplayer.Player.cmd_prefix = mplayer.CmdPrefix.PAUSING_KEEP
        if utils.config.Config().mplayer_executable() is not None:
            mplayer.Player.exec_path = utils.config.Config().mplayer_executable()
        mplayer.Player.introspect()
        self._player = mplayer.Player()
        self._player.args = ['-really-quiet', '-msglevel', 'global=6']

    def __del__(self):
        self._player.quit()

    def isstopped(self):
        return self._player is not None and self.filename() is None and self.length() is None

    def play_list(self, playlist):
        self._player.loadlist(playlist)

    def play(self, filename):
        self._player.loadfile(filename)
        self.fullscreen(True)

    def pause(self):
        self._player.pause()

    def stop(self):
        self._player.stop()

    def seek(self, value, seek_mode=SEEK_MODE_SECONDS_RELATIVE):
        self._player.seek(seek_mode, value)

    def fullscreen(self, value):
        self._player.vo_fullscreen(1 if value else 0)

    def time_pos(self):
        d = self._player.time_pos
        if d is None:
            return self._player.time_pos
        return d

    def percent_pos(self):
        d = self._player.percent_pos
        if d is None:
            return self._player.percent_pos
        return d

    def path(self):
        d = self._player.path
        if d is None:
            return self._player.path
        return self._player.path

    def filename(self):
        d = self._player.filename
        if d is None:
            return self._player.filename
        return d

    def loop(self, value):
        self._player.loop = value

    def length(self):
        d = self._player.length
        if d is None:
            return self._player.length
        return d
