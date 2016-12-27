# -*- coding: utf-8 -*-

import os

import utils.config as config
import xmain


class Wallpaper(object):
    def load(self):
        if os.path.isfile(self.custom_image_path()):
            return self._show(self.custom_image_path())
        else:
            return self._show(self.default_image_path())

    def _show(self, filepath):
        xmain.send({'type': 'show_image', 'path': filepath})
        return True

    def default_image_path(self):
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tools', 'slon-ds-image.png')

    def custom_image_path(self):
        return config.Config().wallpaper_path()
