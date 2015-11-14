# -*- coding: utf-8 -*-


import utils.support as support


class Receiver(object):
    def __init__(self, data):
        command_name = data['command']
        command_class_name = support.underscore_to_camelcase(command_name)
        exec("from .commands.{name} import {klass}".format(name=command_name, klass=command_class_name))
        command_class = eval(command_class_name)
        self._command_object = command_class(data)

    def call(self):
        self._command_object.call()
