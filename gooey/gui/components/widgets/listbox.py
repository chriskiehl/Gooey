from gooey.gui.components.widgets.bases import TextContainer
import wx

from gooey.gui import formatters
from gooey.gui.lang.i18n import _


class Listbox(TextContainer):

    def getWidget(self, parent, *args, **options):
        default = _('select_option')
        return wx.ListBox(
            parent=parent,
            choices=self._meta['choices'],
            size=(-1,60),
            style=wx.LB_MULTIPLE
        )

    def setOptions(self, options):
        self.widget.SetChoices()

    def setValue(self, values):
        for string in values:
            self.widget.SetStringSelection(string)

    def getWidgetValue(self):
        return [self.widget.GetString(index)
                for index in self.widget.GetSelections()]

    def formatOutput(self, metadata, value):
        return formatters.listbox(metadata, value)
