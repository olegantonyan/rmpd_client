# -*- coding: utf-8 -*-

import time
import logging
import os
import threading

import mediaplayer.wrapperplayer
import mediaplayer.playlist
import utils.singleton
import utils.threads
import system.status

log = logging.getLogger(__name__)


class PlayerGuard(object, metaclass=utils.singleton.Singleton):
    def __init__(self):
        self._onchange_lock = threading.Lock()
        self._player = mediaplayer.wrapperplayer.WrapperPlayer()
        self._playlist = None
        self._callbacks = None
        self._check_status()

    def _wait_on_change_decorator(func):
        def wrap(self, *args):
            if self.isstopped():  # wait for poll _check_status
                time.sleep(2.5)
            self._onchange_lock.acquire()
            result = func(self, *args)
            self._onchange_lock.release()
            return result
        return wrap

    def isstopped(self):
        return self._player is not None and self._player.isstopped()

    def set_callbacks(self, **kwargs):
        self._callbacks = kwargs

    def play_list(self, playlist):
        log.info("start playlist '%s'", playlist)
        if not self.isstopped():
            self.stop()
        lst = mediaplayer.playlist.Playlist(playlist)
        self.play(lst.current())
        self._playlist = lst
        # self.__playlist = mediaplayer.playlist.Playlist(playlist)
        # self.play(self.__playlist.current())

    def play(self, filename):
        log.info("start track '%s'", filename)
        if os.path.isfile(filename):
            self._onchange_lock.acquire()
            self._player.play(filename)
            retries = 0
            while self.isstopped():
                time.sleep(0.5)
                retries += 1
                if retries > 10:
                    log.warning("reinitializing mplayer as it has probably crashed")
                    try:
                        self._callbacks["onerror"](message="reinitializing mplayer as it has probably crashed",
                                                   filename=os.path.basename(self._playlist.pick_prev()))
                    except:
                        pass
                    del self._player
                    self._player = mediaplayer.wrapperplayer.WrapperPlayer()
                    self._player.play(filename)
                    retries = 0
            self._onchange_lock.release()
            if self._playlist:
                self._playlist.save_position()
            self._set_playing_status(True)
            try:
                self._callbacks["onplay"](filename=self.filename())
            except:
                pass
        else:
            log.error("file '{f}' does not exists".format(f=filename))
            try:
                self._callbacks["onerror"](message="file does not exists", filename=os.path.basename(filename))
            except:
                pass

    def pause(self):
        log.info("paused/resumed")
        self._player.pause()

    def stop(self):
        log.info("stopped")
        self._player.stop()
        try:
            self._callbacks["onstop"](filename=os.path.basename(self._playlist.current()))
        except:
            pass
        self._playlist = None

    @_wait_on_change_decorator
    def time_pos(self):
        return self._player.time_pos()

    @_wait_on_change_decorator
    def percent_pos(self):
        return self._player.percent_pos()

    @_wait_on_change_decorator
    def filename(self):
        return self._player.filename()

    @_wait_on_change_decorator
    def length(self):
        return self._player.length()

    def quit(self):
        self._player.quit()
        del self._player

    def _check_status(self):
        try:
            is_stopped = self.isstopped()
            if is_stopped and self._playlist is not None:
                log.debug("track finished, about to start a next one")
                self._set_playing_status(False)
                try:
                    self._callbacks["onstop"](filename=os.path.basename(self._playlist.current()))
                except:
                    pass

                self.play(self._playlist.next())
        except:
            log.exception("unhandled exception when checking status")
        finally:
            utils.threads.run_after_timeout(timeout=1.1, target=self._check_status, daemon=True)

    def _set_playing_status(self, status):
        system.status.Status().playing = status
