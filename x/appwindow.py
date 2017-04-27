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

        self.layout = Qt.QGridLayout()
        self.layout.addWidget(self.image_label, 0, 0)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        self.showFullScreen()

    def show_image(self, image_path):
        if image_path is None:
            return self.image_label.clear()
        pixmap = Qt.QPixmap(image_path)
        height = self._height()
        scaled = pixmap.scaledToHeight(height, Qt.Qt.SmoothTransformation)
        self.image_label.setAlignment(Qt.Qt.AlignCenter)
        return self.image_label.setPixmap(scaled)

    def _height(self):
        screen = Qt.QDesktopWidget().screenGeometry()
        return screen.height()

    def _width(self):
        screen = Qt.QDesktopWidget().screenGeometry()
        return screen.width()

