from gooey.gui import formatters
from gooey.gui.components.widgets.bases import TextContainer
from gooey.gui.components.widgets.core.text_input import TextInput


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

