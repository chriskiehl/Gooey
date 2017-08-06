from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame, QWidget, QHBoxLayout, QTabWidget
from PyQt5.QtWidgets import QVBoxLayout
from gooey.gui.components.general import line



class StockLayout(QFrame):
    def __init__(self, header, body, footer):
        super(StockLayout, self).__init__()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(header, alignment=Qt.AlignTop, stretch=0)

        layout.addWidget(line(self, QFrame.HLine))
        layout.setSpacing(0)

        layout.addWidget(body, stretch=1)
        layout.setSpacing(0)

        layout.addWidget(line(self, QFrame.HLine))
        layout.addWidget(footer)

        self.setLayout(layout)
        self.setFrameShape(QFrame.NoFrame)


class WithTabs(QWidget):
    def __init__(self, configPanel, *args, **kwargs):
        super(WithTabs, self).__init__(*args, **kwargs)

        layout = QVBoxLayout()
        tabs = QTabWidget(self)
        tabs.addTab(configPanel, "Required")
        tabs.addTab(QWidget(self), "Optional")
        layout.addWidget(tabs)
        self.setLayout(layout)

class SplitLayout(QWidget):
    """
    Partitions two widgets based on a fixed size [left | right ]
    """
    def __init__(self, parent, left, right, size=200):
        super(SplitLayout, self).__init__(parent)
        self.left = self.withMaxSize(left, size)
        self.line = line(self, QFrame.VLine)
        self.right = right
        self.layoutComponent()

    def layoutComponent(self):
        layout = QHBoxLayout()
        layout.addWidget(self.left, 0)
        layout.addWidget(self.line)
        layout.addWidget(self.right, 1)
        self.setLayout(layout)

    def withMaxSize(self, widget, maxSize):
        '''
        Wraps the target widget in another QWidget so that we
        can limit its max size
        '''
        wrapped = QWidget(self)
        wrapped.setMaximumWidth(maxSize)
        layout = QVBoxLayout()
        layout.addWidget(widget)
        wrapped.setLayout(layout)
        return wrapped

    def hideLeft(self):
        self.left.setVisible(False)
        self.line.setVisible(False)

