# -*- coding: utf-8 -*-

import PyQt5.Qt as Qt


class AppWindow(Qt.QWidget):
    def __init__(self):
        super().__init__()
        self.setBackgroundRole(Qt.QPalette.Base)
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.Qt.black)
        self.setPalette(p)

        self.image_label = Qt.QLabel(self)
        self.image_label.setSizePolicy(Qt.QSizePolicy.Expanding, Qt.QSizePolicy.Expanding)
        self.image_label.setAlignment(Qt.Qt.AlignCenter)

        # l = Qt.QLabel(self)
        # l.setText(" ____________________________________________________________ " + str(self._width()) + 'x' + str(self._height()))

        self.layout = Qt.QGridLayout()
        self.layout.addWidget(self.image_label, 0, 0)
        # self.layout.addWidget(l,0,0)
        self.setLayout(self.layout)
        self.showFullScreen()

    def show_image(self, image_path):
        pixmap = Qt.QPixmap(image_path)
        scaled = pixmap.scaledToHeight(min(self._height(), self._width()))
        self.image_label.setPixmap(scaled)

    def _height(self):
        screen = Qt.QDesktopWidget().screenGeometry()
        return screen.height()

    def _width(self):
        screen = Qt.QDesktopWidget().screenGeometry()
        return screen.width()
