# -*- coding: utf-8 -*-

import mimetypes

import mediaplayer.player.mplayer
import mediaplayer.player.imageplayer
import hardware
import mediaplayer.player.pyomxplayer.pyomxplayer
import utils.config


class PlayerWrapper(object):
    def __init__(self):
        self._mplayer = mediaplayer.player.mplayer.MPlayer()
        self._omxplayer = mediaplayer.player.pyomxplayer.pyomxplayer.OMXPlayer()
        if utils.config.Config().omplayer_executable() is not None:
            self._omxplayer.exec_path = utils.config.Config().omplayer_executable()
        if utils.config.Config().omplayer_arguments() is not None:
            self._omxplayer.args = utils.config.Config().omplayer_arguments()
        self._imageplayer = mediaplayer.player.imageplayer.ImagePlayer()
        self._active_player = NullPlayer()

    def __del__(self):
        if hasattr(self, '_mplayer'):
            del self._mplayer
        if hasattr(self, '_omxplayer'):
            del self._omxplayer
        if hasattr(self, '_omxplayer'):
            del self._imageplayer

    def quit(self):
        self._omxplayer.quit()
        del self._mplayer
        del self._omxplayer
        del self._imageplayer

    def play(self, filename, start_position=0, show_duration=0, mime_type=None):
        if mime_type is None:
            mime_type = self._guess_mime_type(filename)
        if self._isvideo(mime_type) and hardware.platfrom.__name__ == 'raspberry':
            self._active_player = self._omxplayer
        elif self._isaudio(mime_type):
            self._active_player = self._mplayer
        elif self._isvideo(mime_type) and hardware.platfrom.__name__ == 'pc':
            self._active_player = self._mplayer
        elif self._isimage(mime_type):
            self._active_player = self._imageplayer
        return self._active_player.play(filename, start_position, show_duration)

    def stop(self):
        return self._active_player.stop()

    def isstopped(self):
        return self._active_player.isstopped()

    def time_pos(self):
        return self._active_player.time_pos()

    def percent_pos(self):
        return self._active_player.percent_pos()

    def filename(self):
        return self._active_player.filename()

    def length(self):
        return self._active_player.length()

    def _guess_mime_type(self, filename):
        return mimetypes.guess_type(filename)[0]

    def _isvideo(self, mime_type):
        return mime_type.startswith('video/')

    def _isaudio(self, mime_type):
        return mime_type.startswith('audio/')

    def _isimage(self, mime_type):
        return mime_type.startswith('image/')


class NullPlayer(object):
    def play(self, *_):
        return False

    def stop(self):
        return False

    def isstopped(self):
        return True

    def time_pos(self):
        return 0

    def percent_pos(self):
        return 0

    def filename(self):
        return None

    def length(self):
        return 0
