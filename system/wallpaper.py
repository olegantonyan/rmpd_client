# -*- coding: utf-8 -*-

import os

import utils.shell as shell
import utils.singleton
import hardware
import utils.config as config
import xmain


class Wallpaper(object, metaclass=utils.singleton.Singleton):
    def __init__(self):
        self._cpid = None

    def load(self):
        if os.path.isfile(self.custom_image_path()):
            if self.show(self.custom_image_path()):
                return True
            else:
                return self.show(self.default_image_path())
        else:
            return self.show(self.default_image_path())

    def show(self, filepath):
        if hardware.platfrom.__name__ != 'raspberry':
            return True
        xmain.send({'type': 'show_image', 'path': filepath})
        if self._cpid is not None:
            self.hide()
        (r, o, e, p) = shell.execute_child_pid("sudo fbi {} --noverbose -T 1".format(filepath))
        if r == 0:
            self._cpid = p
        return r == 0

    def hide(self):
        if self._cpid is None:
            return False
        (r, o, e) = shell.execute("sudo kill {}".format(self._cpid))
        if r == 0:
            self._cpid = None
        return r == 0

    def default_image_path(self):
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tools', 'slon-ds-image.png')

    def custom_image_path(self):
        return config.Config().wallpaper_path()
