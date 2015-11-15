# -*- coding: utf-8 -*-

import importlib

import utils.support as support


class Sender(object):
    def __init__(self, control_wrapper, command_name):
        command_class_name = support.underscore_to_camelcase(command_name)
        module = importlib.import_module(".outgoing.{name}".format(name=command_name), __package__)
        command_class = getattr(module, command_class_name)
        self._command_object = command_class(control_wrapper)

    def call(self, **kwargs):
        return self._command_object.call(**kwargs)
