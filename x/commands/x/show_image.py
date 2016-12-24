# -*- coding: utf-8 -*-

import x.log as log
import x.commands.x.base_command as base_command


class ShowImage(base_command.BaseCommand):
    def call(self):
        path = self._data['path']
        log.info(__name__, 'setting image from {}'.format(path))
        self._window.show_image(path)
