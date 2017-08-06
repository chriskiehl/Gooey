from PyQt5.QtCore import *
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget

from rx.subjects import Subject


class BaseWidget(QWidget):
    widget_class = None

    def arrange(self, label, text):
        raise NotImplementedError

    def getWidget(self, ):
        return self.widget_class(self)

    def connectSignal(self):
        raise NotImplementedError

    def getSublayout(self, *args, **kwargs):
        raise NotImplementedError

    def setValue(self, value):
        raise NotImplementedError

    def receiveChange(self, *args, **kwargs):
        raise NotImplementedError

    def dispatchChange(self, value, **kwargs):
        raise NotImplementedError

    def formatOutput(self, metatdata, value):
        raise NotImplementedError


class TextContainer(BaseWidget):
    widget_class = None

    def __init__(self, parent, widgetInfo, *args, **kwargs):
        super(TextContainer, self).__init__(parent, *args, **kwargs)

        self._id = widgetInfo['id']
        self._meta = widgetInfo['data']
        self.label = QLabel('<b>{}</b>'.format(widgetInfo['data']['display_name']))
        self.help_text = QLabel(widgetInfo['data']['help'])
        self.widget = self.getWidget()
        self.layout = self.arrange(self.label, self.help_text)
        self.value = Subject()
        self.connectSignal()

    def arrange(self, label, text):
        layout = QVBoxLayout()
        layout.addWidget(label, alignment=Qt.AlignTop)
        if text:
            layout.addWidget(text)
        else:
            layout.addStretch(1)
        layout.addLayout(self.getSublayout())
        return layout

    def getWidget(self,):
        return self.widget_class(self)

    def connectSignal(self):
        self.widget.textChanged.connect(self.dispatchChange)

    def getSublayout(self, *args, **kwargs):
        raise NotImplementedError

    def setValue(self, value):
        raise NotImplementedError

    def receiveChange(self, metatdata, value):
        raise NotImplementedError

    def dispatchChange(self, value, **kwargs):
        raise NotImplementedError

    def formatOutput(self, metadata, value):
        raise NotImplementedError





