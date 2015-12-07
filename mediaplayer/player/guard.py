# -*- coding: utf-8 -*-

import queue
import importlib
import threading
import logging

import utils.singleton
import utils.threads
import utils.support as support

import mediaplayer.wrapperplayer

log = logging.getLogger(__name__)


class Guard(object, metaclass=utils.singleton.Singleton):
    def __init__(self):
        self._player = None
        self._rx = queue.Queue()
        self._tx = queue.Queue()
        self._stop_flag = False
        self._thread = threading.Thread(target=self._serve)
        self._thread.setDaemon(True)
        self._stop_flag = False
        self._thread.start()
        self._expected_state = {'name': 'stopped', 'args': {}}
        self._check_state()

    def execute(self, command, **kwargs):
        self._rx.put((command, kwargs))
        res = self._tx.get()
        return res

    def _serve(self):
        while not self._stop_flag:
            if self._player is None:
                self._init_player()
            result = None
            command, kwargs = None, {}
            try:
                command, kwargs = self._rx.get()
                result = self._dispatch(command, **kwargs)
            except:
                log.exception('error processing player command {name}'.format(name=command))
            finally:
                self._tx.put(result)

    def _dispatch(self, command_name, **kwargs):
        command_class_name = support.underscore_to_camelcase(command_name)
        module = importlib.import_module(".commands.{name}".format(name=command_name), __package__)
        command_class = getattr(module, command_class_name)
        command_object = command_class(self._player_object,
                                       self._set_expected_state,
                                       self._init_player,
                                       self._deinit_player,
                                       **kwargs)
        return command_object.call()

    def _init_player(self):
        self._player = mediaplayer.wrapperplayer.WrapperPlayer()
        return self._player

    def _deinit_player(self):
        del self._player
        self._player = None

    def _player_object(self):
        return self._player

    def _check_state(self):
        try:
            if self._expected_state['name'] == 'playing':
                if self.execute('state') == 'stopped':
                    print('suddenly stopped')
                    print(self._expected_state['args'])
                    log.debug("track finished, about to start a next one")
                    # self._set_playing_status(False)
                    # self._run_callback('onstop', filename=os.path.basename(self._playlist.current()))
        except:
            log.exception("unhandled exception when checking status")
        finally:
            if not self._stop_flag:
                utils.threads.run_after_timeout(timeout=1, target=self._check_state, daemon=True)

    def _set_expected_state(self, state, **kwargs):
        self._expected_state = {'name': state, 'args': kwargs}

    def __del__(self):
        self._stop_flag = True
        try:
            self.execute("quit")  # force execution to fetch from queue
        except:
            pass
