# -*- coding: utf-8 -*-

import logging
import os
import threading

import utils.singleton
import mediaplayer.player.guard as guard
import remotecontrol.protocoldispatcher as proto
import utils.threads

log = logging.getLogger(__name__)


class Watcher(object, metaclass=utils.singleton.Singleton):
    lock = threading.Lock()

    def __init__(self):
        self._callbacks = None
        self._guard = guard.Guard()
        self._expected_state = ('stopped', {})
        self._check_state()

    def play(self, filepath):
        current_expected_state = self._get_expected_state()
        if current_expected_state[0] == 'playing':
            self._guard.execute('stop')
            self._onstop(current_expected_state[1]['filepath'])

        self._set_expected_state('playing', filepath=filepath)
        if self._guard.execute('play', filepath=filepath):
            self._onplay(filepath)
        else:
            self._onerror(filepath, 'unable to start playback, reinitializing player')
            log.error('error starting track {f}'.format(f=filepath))

    def stop(self):
        current_expected_state = self._get_expected_state()
        if current_expected_state[0] != 'stopped':
            self._guard.execute('stop')
            self._set_expected_state('stopped')
            self._onstop(current_expected_state[1].get('filepath'))

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

    @utils.threads.synchronized(lock)
    def set_callbacks(self, **kwargs):
        self._callbacks = kwargs

    @utils.threads.synchronized(lock)
    def _set_expected_state(self, name, **kwargs):
        self._expected_state = (name, kwargs)

    @utils.threads.synchronized(lock)
    def _get_expected_state(self):
        return self._expected_state

    def _check_state(self):
        try:
            expected_state = self._get_expected_state()
            actual_state = self._guard.execute('state')
            if expected_state[0] == 'playing':
                if actual_state == 'stopped':
                    filepath = expected_state[1]['filepath']
                    log.debug('finished track {f}'.format(f=filepath))
                    self._set_expected_state('stopped')
                    self._onstop(filepath)
                    self._run_callback('onfinished', filepath=filepath)
        except:
            log.exception('error checking player state')
        finally:
            utils.threads.run_after_timeout(timeout=0.6, target=self._check_state, daemon=True)

    def _filename_by_path(self, filepath):
        return os.path.basename(filepath)

    def _onplay(self, filepath):
        filename = self._filename_by_path(filepath)
        log.debug("callback on play: " + filename)
        proto.ProtocolDispatcher().send('track_begin', filename=filename)

    def _onstop(self, filepath):
        filename = self._filename_by_path(filepath)
        log.debug("callback on stop: " + filename)
        proto.ProtocolDispatcher().send('track_end', filename=filename)

    def _onerror(self, filepath, message):
        filename = self._filename_by_path(filepath)
        log.debug("callback on error: " + filename + " : " + message)
        proto.ProtocolDispatcher().send('playback_error', filename=filename, message=message)

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

