#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import PyQt5.Qt as Qt

import x.appwindow as appwindow
import utils.shell as shell
import system.wallpaper as wallpaper


def start():
    xauthority = '/tmp/Xauthority'
    interpreter = sys.executable
    pyfile = os.path.abspath(__file__)
    shell.execute_shell('XAUTHORITY={xau} sudo startx {inte} {f} -- -nocursor'.format(xau=xauthority, inte=interpreter, f=pyfile))


def main():
    app = Qt.QApplication(sys.argv)
    win = appwindow.AppWindow()
    win.show_image(wallpaper.Wallpaper().default_image_path())
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
