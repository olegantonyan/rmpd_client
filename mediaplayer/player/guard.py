# -*- coding: utf-8 -*-

import importlib
import logging
import queue
import threading

import mediaplayer.player.commands.base_command as base_command
import mediaplayer.player.playerwrapper as playerwrapper
import utils.singleton as singleton
import utils.support as support
import utils.threads as threads

log = logging.getLogger(__name__)


class Guard(object, metaclass=singleton.Singleton):
    def __init__(self):
        self._player = None
        self._rx = queue.Queue()
        self._tx = queue.Queue()
        self._stop_flag = False
        self._atomic_lock = threading.Lock()
        threads.run_in_thread(self._serve)

    def execute(self, command, **kwargs):
        with self._atomic_lock:
            self._rx.put((command, kwargs))
            return self._tx.get()

    def _serve(self):
        while not self._stop_flag:
            if not self._player_initialized():
                self._init_player()
            result = None
            command, kwargs = None, {}
            try:
                command, kwargs = self._rx.get()
                result = self._dispatch(command, **kwargs)
                if command == 'quit':
                    self._deinit_player()
            except base_command.PlayerError:
                log.exception('reinitializing player after command {name}'.format(name=command))
                self._deinit_player()
                self._init_player()
            except:
                log.exception('error processing player command {name}'.format(name=command))
            finally:
                self._tx.put(result)

    def _dispatch(self, command_name, **kwargs):
        command_class_name = support.underscore_to_camelcase(command_name)
        module = importlib.import_module(".commands.{name}".format(name=command_name), __package__)
        command_class = getattr(module, command_class_name)
        command_object = command_class(self._player_object, **kwargs)
        return command_object.call()

    def _init_player(self):
        self._player = playerwrapper.PlayerWrapper()
        return self._player

    def _deinit_player(self):
        del self._player
        self._player = None

    def _player_initialized(self):
        return self._player is not None

    def _player_object(self):
        return self._player

    def __del__(self):
        self._stop_flag = True
        self.execute("quit")  # force execution to fetch from queue
