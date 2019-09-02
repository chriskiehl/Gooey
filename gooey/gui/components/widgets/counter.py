from gooey.gui.components.widgets.dropdown import Dropdown

from gooey.gui import formatters


class Counter(Dropdown):

    def setValue(self, value):
        index = self._meta['choices'].index(value) + 1
        self.widget.SetSelection(index)

    def formatOutput(self, metadata, value):
        return formatters.counter(metadata, value)
