# -*- coding: utf-8 -*-

import importlib

import utils.support as support


class Dispatcher(object):
    def __init__(self, proc, **kwargs):
        self._proc = proc
        self._kwargs = kwargs

    def call(self, msg):
        command_name = msg['type']
        command_class_name = support.underscore_to_camelcase(command_name)
        module = importlib.import_module(".commands.{proc}.{name}".format(name=command_name, proc=self._proc), __package__)
        command_class = getattr(module, command_class_name)
        command_object = None
        if self._proc == 'x':
            command_object = command_class(msg, **self._kwargs)
        elif self._proc == 'daemon':
            command_object = command_class(msg)
        if command_object is not None:
            command_object.call()
