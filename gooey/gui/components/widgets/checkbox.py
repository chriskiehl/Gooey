import wx

from gooey.gui import formatters, events
from gooey.gui.components.widgets.bases import TextContainer
from gooey.gui.pubsub import pub
from gooey.gui.util import wx_util
from gooey.util.functional import getin


class CheckBox(TextContainer):

    widget_class = wx.CheckBox

    def arrange(self, *args, **kwargs):
        wx_util.make_bold(self.label)
        wx_util.dark_grey(self.help_text)
        wx_util.withColor(self.error, self._options['error_color'])
        self.error.Hide()

        self.help_text.SetMinSize((0,-1))

        layout = wx.BoxSizer(wx.VERTICAL)
        layout.Add(self.label)
        layout.AddSpacer(2)
        layout.AddStretchSpacer(1)
        if self.help_text:
            hsizer = wx.BoxSizer(wx.HORIZONTAL)
            hsizer.Add(self.widget, 0)
            hsizer.Add(self.help_text, 1)
            layout.Add(hsizer, 1, wx.EXPAND)
            layout.AddSpacer(2)
        else:
            layout.Add(self.widget, 0, wx.EXPAND)
            layout.AddStretchSpacer(1)
        return layout


    def setValue(self, value):
        self.widget.SetValue(value)

    def getWidgetValue(self):
        return self.widget.GetValue()


    def formatOutput(self, metatdata, value):
        return formatters.checkbox(metatdata, value)


    def hideInput(self):
        self.widget.Hide()
