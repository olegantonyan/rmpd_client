# -*- coding: utf-8 -*-

import os

import mediaplayer.mplayer
import mediaplayer.pyomxplayer.pyomxplayer
import hardware
import utils.config


class WrapperPlayer(object):
    def __init__(self):
        self._mplayer = mediaplayer.mplayer.MPlayer()
        self._omxplayer = mediaplayer.pyomxplayer.pyomxplayer.OMXPlayer()
        if utils.config.Config().omplayer_executable() is not None:
            self._omxplayer.exec_path = utils.config.Config().omplayer_executable()
        if utils.config.Config().omplayer_arguments() is not None:
            self._omxplayer.args = utils.config.Config().omplayer_arguments()

    def __del__(self):
        del self._mplayer
        del self._omxplayer

    def quit(self):
        self._omxplayer.quit()
        del self._mplayer
        del self._omxplayer

    def _player(self, filename=None):
        if not filename:
            if hardware.platfrom.__name__ == 'raspberry' and not self._omxplayer.isstopped():
                return self._omxplayer
            return self._mplayer
        elif self.isvideo(filename) and hardware.platfrom.__name__ == 'raspberry':
            return self._omxplayer
        return self._mplayer

    def isvideo(self, filename):
        ext = os.path.splitext(filename)[1].replace('.', '')
        if ext in ['mkv', 'mp4', 'avi', 'mpeg2', 'mov', 'mpg']:
            return True
        return False

    def play(self, filename):
        return self._player(filename).play(filename)

    def pause(self):
        return self._player().pause()

    def stop(self):
        return self._player().stop()

    def isstopped(self):
        return self._player().isstopped()

    def time_pos(self):
        return self._player().time_pos()

    def percent_pos(self):
        return self._player().percent_pos()

    def filename(self):
        return self._player().filename()

    def length(self):
        return self._player().length()
