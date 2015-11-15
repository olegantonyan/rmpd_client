# -*- coding: utf-8 -*-

import importlib

import utils.support as support


class Receiver(object):
    def __init__(self, control_wrapper, data, sequence):
        command_name = data['command']
        command_class_name = support.underscore_to_camelcase(command_name)
        module = importlib.import_module(".incoming.{name}".format(name=command_name), __package__)
        command_class = getattr(module, command_class_name)
        self._command_object = command_class(control_wrapper, data, sequence)

    def call(self):
        return self._command_object.call()
