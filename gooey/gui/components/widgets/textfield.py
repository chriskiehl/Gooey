import wx

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

    def syncUiState(self, state: t.TextField):
        textctr: wx.TextCtrl = self.widget.widget
        textctr.SetValue(state['value'])
        textctr.SetHint(state['placeholder'])
        textctr.Enable(state['enabled'])
        self.Show(state['visible'])
        if state['error']:
            self.setErrorString(state['error'])
