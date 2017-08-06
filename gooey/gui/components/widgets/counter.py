from gooey.gui.components.widgets.dropdown import Dropdown
from gooey.gui import formatters

class Counter(Dropdown):

    def formatOutput(self, metadata, value):
        return formatters.counter(metadata, value)
