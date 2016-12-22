#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import PyQt5.Qt as qt


class AppWindow(qt.QWidget):
    def __init__(self):
        super().__init__()
        self.setBackgroundRole(qt.QPalette.Base)
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), qt.Qt.black)
        self.setPalette(p)

        self.image_label = qt.QLabel(self)
        self.image_label.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Expanding)
        self.image_label.setAlignment(qt.Qt.AlignCenter)

        self.layout = qt.QGridLayout()
        self.layout.addWidget(self.image_label, 0, 0)
        self.setLayout(self.layout)
        self.showFullScreen()

    def show_image(self, image_path):
        pixmap = qt.QPixmap(image_path)
        scaled = pixmap.scaledToHeight(min(self._height(), self._width()))
        self.image_label.setPixmap(scaled)

    def _height(self):
        screen = qt.QDesktopWidget().screenGeometry()
        return screen.height()

    def _width(self):
        screen = qt.QDesktopWidget().screenGeometry()
        return screen.width()


def default_image_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tools', 'slon-ds-image.png')


def main():
    app = qt.QApplication(sys.argv)
    win = AppWindow()
    win.show_image(default_image_path())

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
