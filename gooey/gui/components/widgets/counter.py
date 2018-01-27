from gooey.gui.components.widgets.dropdown import Dropdown

from gooey.gui import formatters


class Counter(Dropdown):

    def setValue(self, value):
        self.widget.SetSelection(value)

    def getWidgetValue(self):
        return self.widget.GetValue()


    def formatOutput(self, metadata, value):
        return formatters.counter(metadata, value)
