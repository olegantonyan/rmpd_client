# -*- coding: utf-8 -*-

import time
import logging
import os
import threading
import traceback

import mediaplayer.wrapperplayer
import mediaplayer.playlist.playlist as playlist
import utils.singleton
import utils.threads
import system.status

log = logging.getLogger(__name__)


class PlayerGuard(object, metaclass=utils.singleton.Singleton):
    def __init__(self, **kwargs):
        self._onchange_lock = threading.Lock()
        self._init_player_object()
        self._playlist = None
        self._callbacks = kwargs  # TODO thread-safety
        self._check_status()

    def _wait_on_change_decorator(func):
        def wrap(self, *args):
            if self.isstopped():  # wait for poll _check_status
                time.sleep(2.5)
            self._onchange_lock.acquire()
            try:
                return func(self, *args)
            finally:
                self._onchange_lock.release()
        return wrap

    def isstopped(self):
        return self._player is not None and self._player.isstopped()

    def play_list(self):
        if not self.isstopped():
            self.stop()
        log.info("start playlist")
        lst = playlist.Playlist()
        self.play(lst.current())
        self._playlist = lst

    def play(self, filename):
        if filename is None:
            return
        log.info("start track '%s'", filename)
        if not os.path.isfile(filename):
            log.error("file '{f}' does not exists".format(f=filename))
            self._run_callback('onerror', message="file does not exists", filename=os.path.basename(filename))
            return
        self._try_play(filename)
        if self._playlist:
            self._playlist.save_position()
        self._set_playing_status(True)
        self._run_callback('onplay', filename=self.filename())

    def pause(self):
        log.info("paused/resumed")
        self._player.pause()

    def stop(self):
        log.info("stopped")
        self._player.stop()
        self._run_callback('onstop', filename=os.path.basename(self._playlist.current()))
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
                self._run_callback('onstop', filename=os.path.basename(self._playlist.current()))
                self.play(self._playlist.next())
        except:
            log.exception("unhandled exception when checking status:\n{ex}".format(ex=traceback.format_exc()))
        finally:
            utils.threads.run_after_timeout(timeout=1.1, target=self._check_status, daemon=True)

    def _set_playing_status(self, status):
        system.status.Status().playing = status

    def _init_player_object(self):
        self._player = mediaplayer.wrapperplayer.WrapperPlayer()
        return self._player

    def _run_callback(self, name, **kwargs):
        cb = self._callbacks.get(name)
        if cb is None:
            return
        try:
            return cb(**kwargs)
        except:
            log.warning("error running {name} callback:{ex}\n".format(name=name, ex=traceback.format_exc()))

    def _try_play(self, filename):
        self._onchange_lock.acquire()
        try:
            self._player.play(filename)
            retries = 0
            while self.isstopped():
                time.sleep(0.5)
                retries += 1
                if retries > 10:
                    msg = "reinitializing mplayer as it has probably crashed"
                    log.warning(msg)
                    self._run_callback('onerror', message=msg, filename=os.path.basename(self._playlist.pick_prev()))
                    del self._player
                    self._init_player_object()
                    self._player.play(filename)
                    retries = 0
        finally:
            self._onchange_lock.release()
