# -*- coding: utf-8 -*-

import logging
import os
import time
import threading

import utils.singleton as singleton
import mediaplayer.player.guard as guard
import utils.threads as threads
import remotecontrol.protocoldispatcher as proto

log = logging.getLogger(__name__)


class Watcher(object, metaclass=singleton.Singleton):
    lock = threading.RLock()

    def __init__(self):
        self._callbacks = None
        self._guard = guard.Guard()
        self._expected_state = ('stopped', {})
        self._stop_flag = False
        threads.run_in_thread(self._check_state)

    @threads.synchronized(lock)
    def play(self, item):
        if item is None:
            return False

        if self.isplaying():
            self._guard.execute('stop')
            self._onstop(self._get_expected_state()[1]['item'])
        if self._guard.execute('play', filepath=item.filepath):
            self._onplay(item)
            self._set_expected_state('playing', item=item)
            return True
        else:
            self._onerror(item, 'unable to start playback, reinitializing player')
            log.error('error starting track {f}'.format(f=item.filepath))
            self._run_callback('onerror', item=item)
            return False

    @threads.synchronized(lock)
    def resume(self, item, position_seconds):
        if item is None or position_seconds is None:
            return False

        if self.isplaying():
            log.error('cannot resume from playing state')
            return False

        if self._guard.execute('play', filepath=item.filepath, start_position=position_seconds):
            self._onresume(item, position_seconds)
            self._set_expected_state('playing', item=item)
            return True
        else:
            self._onerror(item, 'unable to resume playback, reinitializing player')
            log.error('error resuming track {f}'.format(f=item.filepath))
            self._run_callback('onerror', item=item)
            return False

    @threads.synchronized(lock)
    def suspend(self):
        current_expected_state = self._get_expected_state()
        current_time_pos = self.time_pos()
        self._guard.execute('stop')
        item = current_expected_state[1]['item']
        self._onsuspend(item, current_time_pos)
        self._set_expected_state('stopped')
        return item

    @threads.synchronized(lock)
    def isplaying(self):
        return self._get_expected_state()[0] == 'playing'

    @threads.synchronized(lock)
    def stop(self):
        current_expected_state = self._get_expected_state()
        if current_expected_state[1].get('item'):
            self._onstop(current_expected_state[1].get('item'))
        self._guard.execute('stop')
        self._set_expected_state('stopped')

    def time_pos(self):
        return self._guard.execute('time_pos')

    def percent_pos(self):
        return self._guard.execute('percent_pos')

    def filename(self):
        return self._guard.execute('filename')

    def length(self):
        return self._guard.execute('length')

    def quit(self):
        return self._guard.execute('quit')

    @threads.synchronized(lock)
    def set_callbacks(self, **kwargs):
        self._callbacks = kwargs

    @threads.synchronized(lock)
    def _set_expected_state(self, name, **kwargs):
        self._expected_state = (name, kwargs)

    @threads.synchronized(lock)
    def _get_expected_state(self):
        return self._expected_state

    def _check_state(self):
        while not self._stop_flag:
            try:
                expected_state = self._get_expected_state()
                actual_state = self._guard.execute('state')
                if expected_state[0] == 'playing':
                    if actual_state == 'stopped':
                        item = expected_state[1]['item']
                        log.debug('finished track {f}'.format(f=item.filepath))
                        self._set_expected_state('stopped')
                        self._onstop(item)
                        self._run_callback('onfinished', item=item)
            except:
                log.exception('error checking player state')
            time.sleep(0.2)

    def _filename_by_path(self, filepath):
        return os.path.basename(filepath)

    def _onplay(self, item):
        log.debug("on play: " + item.filename)
        proto.ProtocolDispatcher().send('track_begin', item=item)

    def _onstop(self, item):
        log.debug("on stop: " + item.filename)
        proto.ProtocolDispatcher().send('track_end', item=item)

    def _onerror(self, item, message):
        log.debug("on error: " + item.filename + " : " + message)
        proto.ProtocolDispatcher().send('playback_error', item=item, message=message)

    def _onsuspend(self, item, position_seconds):
        log.debug("on suspend: " + item.filename + " (at {} seconds)".format(position_seconds))
        proto.ProtocolDispatcher().send('track_suspend', item=item, position_seconds=position_seconds)

    def _onresume(self, item, position_seconds):
        log.debug("on resume: " + item.filename + " (from {} seconds)".format(position_seconds))
        proto.ProtocolDispatcher().send('track_resume', item=item, position_seconds=position_seconds)

    @threads.synchronized(lock)
    def _run_callback(self, name, **kwargs):
        if self._callbacks is None:
            return
        cb = self._callbacks.get(name)
        if cb is None:
            return
        try:
            return cb(**kwargs)
        except:
            log.exception("error running {name} callback".format(name=name))

    def __del__(self):
        self._stop_flag = True

