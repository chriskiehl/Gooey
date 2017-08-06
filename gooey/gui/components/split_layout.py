from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QFrame
from PyQt5.QtWidgets import QWidget

from gooey.gui.components.general import line, withMaxSize


class SplitLayout(QWidget):
    """
    Partitions two widgets based on a fixed size [left | right ]
    """
    def __init__(self, parent, left, right, size=200):
        super(SplitLayout, self).__init__(parent)
        self.left = withMaxSize(self, left, size)
        self.right = right
        self.layoutComponent()


    def layoutComponent(self):
        layout = QHBoxLayout()
        layout.addWidget(self.left, 0)
        layout.addWidget(line(self, QFrame.VLine))
        layout.addWidget(self.right, 1)
        self.setLayout(layout)



