# -*- coding: utf-8 -*-

import x.commands.daemon.base_command as base_command


class Log(base_command.BaseCommand):
    def call(self):
        print(self._data)
