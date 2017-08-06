import os
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout


class Header(QFrame):


    def __init__(self, parent, *args, **kwargs):
        super(Header, self).__init__(parent, *args, **kwargs)

        self.title = QLabel(self)
        self.subtitle = QLabel(self)
        self.icon = QPixmap()
        self.iconLabel = QLabel(self)
        self.layoutComponent()

    def layoutComponent(self):
        layout = QHBoxLayout()
        layout.addLayout(self.format_header(self.title, self.subtitle), stretch=1)
        layout.addWidget(self.iconLabel)

        self.setLayout(layout)
        self.setObjectName('headerSection')
        self.setMaximumHeight(80)
        self.setMinimumWidth(130)
        self.setFrameShape(QFrame.NoFrame)
        self.setLineWidth(0)

    def format_header(self, title, subtitle):
        layout = QVBoxLayout()
        layout.addStretch(1)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addStretch(1)
        return layout

    def setTitle(self, value):
        self.title.setText('<b>{}</b>'.format(value))

    def setSubtitle(self, value):
        self.subtitle.setText(value)

    def setIcon(self, iconPath):
        self.icon.load(os.path.join(os.getcwd(), iconPath))
        self.icon = self.icon.scaled(131, 79, QtCore.Qt.KeepAspectRatio, 1)
        self.iconLabel.setPixmap(self.icon)
