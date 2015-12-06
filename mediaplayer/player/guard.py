# -*- coding: utf-8 -*-

import queue
import importlib
import threading
import logging

import utils.singleton
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

    def execute(self, command, **kwargs):
        self._rx.put((command, kwargs))
        res = self._tx.get()
        return res

    def _serve(self):
        if self._player is None:
            pass
            # self._player = mediaplayer.wrapperplayer.WrapperPlayer()
        while not self._stop_flag:
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
        command_object = command_class(self._player, **kwargs)
        return command_object.call()

    def __del__(self):
        self._stop_flag = True
        try:
            self.execute("quit")  # force execution to fetch from queue
        except:
            pass


class Result(object):
    def __init__(self, ok=False, value={}, message=''):
        self._ok = ok
        self._value = value
        self._message = message

    @property
    def ok(self):
        return self._ok

    @ok.setter
    def ok(self, arg):
        self._ok = arg

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, arg):
        self._value = arg

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, arg):
        self._message = arg
