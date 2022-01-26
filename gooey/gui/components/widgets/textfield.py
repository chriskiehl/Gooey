import wx  # type: ignore

from gooey.gui import formatters
from gooey.gui.components.widgets.bases import TextContainer
from gooey.gui.components.widgets.core.text_input import TextInput
from gooey.python_bindings import types as t

class TextField(TextContainer):
    widget_class = TextInput

    def getWidgetValue(self):
        return self.widget.getValue()

    def setValue(self, value):
        self.widget.setValue(str(value))

    def setPlaceholder(self, value):
        self.widget.SetHint(value)

    def formatOutput(self, metatdata, value):
        return formatters.general(metatdata, value)

    def syncUiState(self, state: t.TextField):  # type: ignore
        textctr: wx.TextCtrl = self.widget.widget
        textctr.SetValue(state['value'])
        textctr.SetHint(state['placeholder'])
        textctr.Enable(state['enabled'])
        self.Show(state['visible'])
        self.error.SetLabel(state['error'] or '')
        self.error.Show(state['error'] is not None and state['error'] is not '')
        self.Layout()
