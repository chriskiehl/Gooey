import wx

from gooey.gui.util.filedrop import FileDrop
from gooey.util.functional import merge
from gooey.gui.components.mouse import notifyMouseEvent


class TextInput(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        super(TextInput, self).__init__(parent)
        self.widget = wx.TextCtrl(self, *args, **kwargs)
        dt = FileDrop(self.widget)
        self.widget.SetDropTarget(dt)
        self.widget.SetMinSize((0, -1))
        self.widget.SetDoubleBuffered(True)
        self.widget.AppendText('')
        self.layout()

        self.widget.Bind(wx.EVT_LEFT_DOWN, notifyMouseEvent)

    def layout(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.widget, 0, wx.EXPAND)
        self.SetSizer(sizer)


    def setValue(self, value):
        self.widget.Clear()
        self.widget.AppendText(str(value))
        self.widget.SetInsertionPoint(0)

    def getValue(self):
        return self.widget.GetValue()

    def SetHint(self, value):
        self.widget.SetHint(value)

    def SetDropTarget(self, target):
        self.widget.SetDropTarget(target)



def PasswordInput(_, parent, *args, **kwargs):
    style = {'style': wx.TE_PASSWORD}
    return TextInput(parent, *args, **merge(kwargs, style))


def MultilineTextInput(_, parent, *args, **kwargs):
    style = {'style': wx.TE_MULTILINE}
    return TextInput(parent, *args, **merge(kwargs, style))
