from PyQt5.QtCore import *
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QVBoxLayout

from gooey.gui.components.widgets.bases import BaseWidget
from gooey.gui import formatters
from rx.subjects import Subject



class CheckBox(BaseWidget):

    def __init__(self, parent, widgetInfo, *args, **kwargs):
        super(CheckBox, self).__init__(parent, *args, **kwargs)
        self._id = widgetInfo['id']
        self._meta = widgetInfo['data']
        self.label = QLabel('<b>{}</b>'.format(widgetInfo['data']['display_name']))
        self.widget = QCheckBox(widgetInfo['data']['help'] or '')

        self.layout = self.arrange()
        self.value = Subject()
        self.connectSignal()

        if widgetInfo['data']['default']:
            self.setValue(widgetInfo['data']['default'])

    def arrange(self):
        layout = QVBoxLayout()
        layout.addWidget(self.label, alignment=Qt.AlignTop)
        layout.addWidget(self.widget)
        return layout

    def connectSignal(self):
        self.widget.stateChanged.connect(self.dispatchChange)

    def setValue(self, value):
        self.widget.setChecked(value)

    def dispatchChange(self, value, **kwargs):
        self.value.on_next({
            'id': self._id,
            'cmd': self.formatOutput(self._meta, self.widget.checkState()),
            'rawValue': self.widget.checkState(),
        })

    def formatOutput(self, metatdata, value):
        return formatters.checkbox(metatdata, value)
