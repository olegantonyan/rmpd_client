# -*- coding: utf-8 -*-

import x.commands.x.base_command as base_command


class ShowImage(base_command.BaseCommand):
    def call(self):
        print(self._data)
