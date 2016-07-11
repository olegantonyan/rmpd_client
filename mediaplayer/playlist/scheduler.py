# -*- coding: utf-8 -*-

import logging
import threading
import queue

import utils.singleton
import utils.threads
import utils.datetime
import mediaplayer.player.watcher as player

log = logging.getLogger(__name__)


class Scheduler(object, metaclass=utils.singleton.Singleton):
    lock = threading.RLock()

    def __init__(self):
        self._player = player.Watcher()
        self._playlist = None
        self._now_playing = None
        self._rx = queue.Queue()
        self._player.set_callbacks(onfinished=self.onfinished)
        self._stop_flag = False
        self._preempted_item = None
        utils.threads.run_in_thread(self._loop)

    def set_playlist(self, playlist):
        log.info("start playlist")
        self._playlist = playlist
        if self._player.isplaying():
            self._play(None)
        self._play(self._playlist.current_background())
        self._schedule()

    def onfinished(self, **kwargs):
        finished_track = kwargs.get('item')
        if finished_track is not None:
            log.info("track finished {f}".format(f=finished_track.filename))
        current_track = self._get_now_playing()
        self._notify_playlist_on_track_end(current_track)
        self._set_now_playing(None)
        self._schedule()

    def _play(self, item):
        if item is None:
            self._set_now_playing(None)
            self._player.stop()
            return False
        if self._player.isplaying():
            if item.is_advertising:
                self._preempt(self._get_now_playing(), self._player.time_pos())  # assert self._get_now_playing() == self._player._get_expected_state()[1]
                self._player.suspend()
            else:
                self._player.stop()
        ok = self._player.play(item)
        self._set_now_playing(item if ok else None)
        return ok

    def _resume(self, item, position):
        ok = self._player.resume(item, position)
        if ok:
            self._set_now_playing(item)
        else:
            self._set_now_playing(None)
            self._reset_preempted()
        return ok

    @utils.threads.synchronized(lock)
    def _set_now_playing(self, item):
        self._now_playing = item

    @utils.threads.synchronized(lock)
    def _get_now_playing(self):
        return self._now_playing

    def _notify_playlist_on_track_end(self, track):
        if self._playlist is not None:
            self._playlist.onfinished(track)

    def _schedule(self, arg=None):
        self._rx.put(arg)

    def _loop(self):
        while not self._stop_flag:
            try:
                self._rx.get(block=True, timeout=1)
            except queue.Empty:
                pass
            if self._playlist is not None:
                self._scheduler()

    def _scheduler(self):
        current_track = self._get_now_playing()

        next_advertising = self._playlist.next_advertising()
        if next_advertising is not None:
            if current_track is None or current_track.is_background:
                if current_track is None:
                    self._notify_playlist_on_track_end(current_track)
                self._play(next_advertising)
        else:
            preempted = self._preempted()
            if preempted:
                if current_track is None:
                    log.info("track resumed '{}' at {}".format(preempted[0].filename, preempted[1]))
                    self._resume(preempted[0], preempted[1])
                    self._reset_preempted()
            else:
                next_background = self._playlist.next_background()
                if next_background is not None:
                    if current_track is None:
                        self._play(next_background)

    def _preempt(self, item, time_pos):
        time_pos = int(time_pos)
        log.info("track suspended '{}' at {}".format(item.filename, time_pos))
        self._preempted_item = (item, time_pos)

    def _preempted(self):
        return self._preempted_item

    def _reset_preempted(self):
        self._preempted_item = None

    def __del__(self):
        self._stop_flag = True

