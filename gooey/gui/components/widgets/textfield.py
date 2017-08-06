
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLineEdit

from gooey.gui.components.widgets.bases import TextContainer
from gooey.gui import formatters


class TextField(TextContainer):
    widget_class = QLineEdit

    def getSublayout(self, *args, **kwargs):
        layout = QHBoxLayout()
        layout.addWidget(self.widget)
        return layout

    def setValue(self, value):
        self.widget.setText(value)

    def connectSignal(self):
        self.widget.textChanged.connect(self.dispatchChange)

    def dispatchChange(self, value, **kwargs):
        self.value.on_next({
            'id': self._id,
            'cmd': self.formatOutput(self._meta, value),
            'rawValue': value
        })

    def formatOutput(self, metatdata, value):
        return formatters.general(metatdata, value)

