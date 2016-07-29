# -*- coding: utf-8 -*-

import logging
import threading
import queue

import utils.singleton as singleton
import mediaplayer.player.guard as guard
import utils.threads as threads
import remotecontrol.protocoldispatcher as proto
import mediaplayer.player.watchdog as wdt

log = logging.getLogger(__name__)


class Watcher(object, metaclass=singleton.Singleton):
    def __init__(self):
        self._callbacks = None
        self._guard = guard.Guard()
        self._expected_state = ('stopped', {})
        self._stop_flag = False
        self._watchdog = wdt.Watchdog()
        self._rx = queue.Queue()
        self._tx = queue.Queue()
        self._atomic_lock = threading.Lock()
        threads.run_in_thread(self._check_state_loop)

    def play(self, item):
        return self._execute('play', {'item': item})

    def resume(self, item, position_seconds):
        return self._execute('resume', {'item': item, 'position_seconds': position_seconds})

    def suspend(self):
        return self._execute('suspend')

    def stop(self):
        return self._execute('stop')

    def isplaying(self):
        return self._execute('isplaying')

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

    def set_callbacks(self, **kwargs):
        self._callbacks = kwargs

    def _execute(self, command, args=None):
        with self._atomic_lock:
            self._rx.put((command, args))
            return self._tx.get()

    def _set_expected_state(self, name, **kwargs):
        self._expected_state = (name, kwargs)

    def _get_expected_state(self):
        return self._expected_state

    def _check_state_loop(self):
        while not self._stop_flag:
            result = None
            try:
                command, kwargs = self._rx.get(block=True, timeout=0.5)
                if command == 'play':
                    result = self._play(kwargs['item'])
                elif command == 'resume':
                    result = self._resume(kwargs['item'], kwargs['position_seconds'])
                elif command == 'suspend':
                    result = self._suspend()
                elif command == 'stop':
                    result = self._stop()
                elif command == 'isplaying':
                    result = self._isplaying()
                self._tx.put(result)
            except queue.Empty:
                self._check_state()
            except:
                log.exception('error running player watcher command')
                self._tx.put(None)

    def _check_state(self):
        try:
            finished_item = self._check_state_get_finished()
            if finished_item is not None:
                self._onstop(finished_item)
                self._run_callback('onfinished', item=finished_item)
        except:
            log.exception('error checking player state')

    def _check_state_get_finished(self):
        expected_state = self._get_expected_state()
        actual_state = self._guard.execute('state')
        if expected_state[0] == 'playing':
            if actual_state == 'stopped':
                item = expected_state[1]['item']
                log.debug('finished track {f}'.format(f=item.filepath))
                self._set_expected_state('stopped')
                return item
        return None

    def _onplay(self, item):
        log.debug("on play: " + item.filename)
        proto.ProtocolDispatcher().send('track_begin', item=item)

    def _onstop(self, item):
        log.debug("on stop: " + item.filename)
        proto.ProtocolDispatcher().send('track_end', item=item)

    def _onerror(self, item, message):
        log.debug("on error: " + item.filename + " : " + message)
        self._watchdog.reset()
        proto.ProtocolDispatcher().send('playback_error', item=item, message=message)

    def _onsuspend(self, item, position_seconds):
        log.debug("on suspend: " + item.filename + " (at {} seconds)".format(position_seconds))
        proto.ProtocolDispatcher().send('track_suspend', item=item, position_seconds=position_seconds)

    def _onresume(self, item, position_seconds):
        log.debug("on resume: " + item.filename + " (from {} seconds)".format(position_seconds))
        proto.ProtocolDispatcher().send('track_resume', item=item, position_seconds=position_seconds)

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

    def _play(self, item):
        if item is None:
            log.error('cannot play none item')
            return False

        if self._isplaying():
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

    def _resume(self, item, position_seconds):
        if item is None or position_seconds is None:
            log.error('cannot resume none item or position ({i} at {p})'.format(i=str(item), p=str(position_seconds)))
            return False

        if self._isplaying():
            log.error('cannot resume from playing state')
            return False

        if not self._watchdog.is_ok_to_resume(item, position_seconds):
            self._onerror(item, 'resumed position is the same as previous, the player probably hangs')
            log.error('resumed position is the same as previous, the player probably hangs: {}'.format(item.filename))
            self._run_callback('onerror', item=item)
            return False

        if self._guard.execute('play', filepath=item.filepath, start_position=position_seconds):
            self._onresume(item, position_seconds)
            self._set_expected_state('playing', item=item)
            self._watchdog.resumed_at(item, position_seconds)
            return True
        else:
            self._onerror(item, 'unable to resume playback, reinitializing player')
            log.error('error resuming track {f}'.format(f=item.filepath))
            self._run_callback('onerror', item=item)
            return False

    def _suspend(self):
        current_expected_state = self._get_expected_state()
        current_time_pos = int(self.time_pos())
        self._guard.execute('stop')
        item = current_expected_state[1]['item']
        self._onsuspend(item, current_time_pos)
        self._set_expected_state('stopped')
        return item

    def _isplaying(self):
        return self._get_expected_state()[0] == 'playing'

    def _stop(self):
        current_expected_state = self._get_expected_state()
        if current_expected_state[1].get('item'):
            self._onstop(current_expected_state[1].get('item'))
        ok = self._guard.execute('stop')
        self._set_expected_state('stopped')
        return ok

    def __del__(self):
        self._stop_flag = True

