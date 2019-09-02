import wx
from functools import reduce

from gooey.gui.components.widgets.core.text_input import MultilineTextInput
from gooey.gui.components.widgets.textfield import TextField
from gooey.gui.components.widgets.bases import TextContainer
from gooey.gui import formatters


class Textarea(TextContainer):

    def getWidget(self, parent, *args, **options):
        widgetHeight = self._options.get('height', -1)
        return wx.TextCtrl(
            parent=parent,
            size=(-1, widgetHeight),
            style=self.getModifiers()
        )

    def getModifiers(self):
        readonly = (wx.TE_READONLY
                    if self._options.get('readonly', False)
                    # using TE_MUTLI as a safe OR-able no-op value
                    else wx.TE_MULTILINE)
        return reduce(lambda acc, val: acc | val, [wx.TE_MULTILINE, readonly])

    def getWidgetValue(self):
        return self.widget.GetValue()

    def setValue(self, value):
        self.widget.Clear()
        self.widget.AppendText(str(value))
        self.widget.SetInsertionPoint(0)

    def formatOutput(self, metatdata, value):
        return formatters.general(metatdata, value)


