from gooey.gooey.gui.components.widgets.textfield import TextField
from gooey.gooey.gui import formatters

class Counter(TextField):

    def formatOutput(self, metadata, value):
        return formatters.commandField(metadata, value)
