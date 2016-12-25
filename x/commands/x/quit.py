# -*- coding: utf-8 -*-

import time
import PyQt5.Qt as Qt

import x.log as log
import x.commands.x.base_command as base_command


class Quit(base_command.BaseCommand):
    def call(self):
        log.info(__name__, 'quiting x')  # just to cause a pipe read
        time.sleep(1)
        Qt.QApplication.quit()
