# -*- coding: utf-8 -*-

import logging
import queue

import utils.singleton
import utils.threads
import utils.datetime
import mediaplayer.player.watcher as player

log = logging.getLogger(__name__)


class Scheduler(object, metaclass=utils.singleton.Singleton):
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
        self._schedule('start_playlist')

    def onfinished(self, **kwargs):
        finished_track = kwargs.get('item')
        if finished_track is not None:
            log.info("track finished {f}".format(f=finished_track.filename))
        self._schedule('track_finished')

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
        if ok:
            self._set_now_playing(item)
        else:
            self._set_now_playing(None)
            self._notify_playlist_on_track_end(item)
        return ok

    def _resume(self, item, position):
        ok = self._player.resume(item, position)
        if ok:
            self._set_now_playing(item)
        else:
            self._set_now_playing(None)
            self._reset_preempted()
            self._notify_playlist_on_track_end(item)
        return ok

    def _set_now_playing(self, item):
        log.debug('set now playing {}'.format(str(item)))
        self._now_playing = item

    def _get_now_playing(self):
        return self._now_playing

    def _notify_playlist_on_track_end(self, track):
        if self._playlist is not None:
            try:
                self._playlist.onfinished(track)
            except:
                log.exception('error notifying playlist on track finished')

    def _schedule(self, arg=None):
        self._rx.put(arg)

    def _loop(self):
        while not self._stop_flag:
            try:
                command = self._rx.get(block=True, timeout=1)
                if command == 'start_playlist':
                    self._start_playlist()
                elif command == 'track_finished':
                    self._track_finished()
            except queue.Empty:
                pass
            except:
                log.exception('error processing scheduler command')
            finally:
                if self._playlist is not None:
                    try:
                        self._scheduler()
                    except:
                        log.exception('error running scheduler')

    def _track_finished(self):
        current_track = self._get_now_playing()
        self._notify_playlist_on_track_end(current_track)
        self._set_now_playing(None)

    def _start_playlist(self):
        if self._player.isplaying():
            self._play(None)
        self._set_now_playing(None)  # for sure
        self._reset_preempted()
        start_item = self._playlist.fisrt_background()
        if start_item is None:
            log.info('no appropriate track to start playlist from')
        else:
            self._play(start_item)

    def _scheduler(self):
        current_track = self._get_now_playing()

        next_advertising = self._playlist.next_advertising()
        if next_advertising is not None:
            # log.debug("next advertising: {a}, current: {c}".format(a=next_advertising, c=current_track))
            if current_track is None or current_track.is_background:
                if current_track is None:
                    self._notify_playlist_on_track_end(current_track)
                self._play(next_advertising)
        else:
            preempted = self._preempted()
            if preempted:
                # log.debug("preempted track: {p}, current: {c}".format(p=preempted[0].filename, c=current_track))
                if current_track is None:
                    log.info("track resumed '{}' at {}".format(preempted[0].filename, preempted[1]))
                    self._resume(preempted[0], preempted[1])
                    self._reset_preempted()
            else:
                next_background = self._playlist.next_background()
                # log.debug("next background: {n}, current: {c}".format(n=next_background, c=current_track))
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
        log.debug('reset preempted state')
        self._preempted_item = None

    def __del__(self):
        self._stop_flag = True

