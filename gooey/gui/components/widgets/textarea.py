from PyQt5.QtWidgets import QTextEdit

from gooey.gui.components.widgets.textfield import TextField


class Textarea(TextField):
    widget_class = QTextEdit

    def setValue(self, value):
        self.value.document().setPlainText(value)

    def dispatchChange(self, *args, **kwargs):
        self.value.on_next({
            'id': self._id,
            'cmd': self.formatOutput(self._meta, self.widget.toPlainText()),
            'value':  self.widget.toPlainText(),
        })
