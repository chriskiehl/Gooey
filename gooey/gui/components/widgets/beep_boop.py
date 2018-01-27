import wx

import wx.lib.inspection
from gooey.gui.components.widgets.textfield import TextField
from gooey.gui.components.widgets.textarea import Textarea
from gooey.gui.components.widgets.password import PasswordField
from gooey.gui.components.widgets.choosers import FileChooser, FileSaver, DirChooser, DateChooser
from gooey.gui.components.widgets.dropdown import Dropdown
from gooey.gui.components.widgets.listbox import Listbox


class CCC(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(CCC, self).__init__(*args, **kwargs)
        x = {'data':{'choices':['one', 'tw'], 'display_name': 'foo', 'help': 'bar', 'commands': ['-t']}, 'id': 1, 'options': {}}

        a = TextField(self, x)
        c = Textarea(self, x)
        b = PasswordField(self, x)
        d = DirChooser(self, x)
        e = FileChooser(self,x)
        f = FileSaver(self, x)
        g = DateChooser(self, x)
        h = Dropdown(self, x)
        i = Listbox(self, x)

        s = wx.BoxSizer(wx.VERTICAL)
        s.Add(a, 0, wx.EXPAND)
        s.Add(b, 0, wx.EXPAND)
        s.Add(c, 0, wx.EXPAND)
        s.Add(d, 0, wx.EXPAND)
        s.Add(e, 0, wx.EXPAND)
        s.Add(f, 0, wx.EXPAND)
        s.Add(g, 0, wx.EXPAND)
        s.Add(h, 0, wx.EXPAND)
        s.Add(i, 0, wx.EXPAND)

        self.SetSizer(s)





app = wx.App()

frame = CCC(None, -1, 'simple.py')
frame.Show()

app.MainLoop()


# import wx
#
# class MainWindow(wx.Frame):
#     def __init__(self, *args, **kwargs):
#         wx.Frame.__init__(self, *args, **kwargs)
#
#         self.panel = wx.Panel(self)
#
#         self.label = wx.StaticText(self.panel, label="Label")
#         self.text = wx.TextCtrl(self.panel)
#         self.button = wx.Button(self.panel, label="Test")
#
#         self.button1 = wx.Button(self.panel, label="ABOVE")
#         self.button2 = wx.Button(self.panel, label="BELLOW")
#
#         self.horizontal = wx.BoxSizer()
#         self.horizontal.Add(self.label, flag=wx.CENTER)
#         self.horizontal.Add(self.text, proportion=1, flag=wx.CENTER)
#         self.horizontal.Add(self.button, flag=wx.CENTER)
#
#         self.vertical = wx.BoxSizer(wx.VERTICAL)
#         self.vertical.Add(self.button1, flag=wx.EXPAND)
#         self.vertical.Add(self.horizontal, proportion=1, flag=wx.EXPAND)
#         self.vertical.Add(self.button2, flag=wx.EXPAND)
#
#         self.panel.SetSizerAndFit(self.vertical)
#         self.Show()
#
#
# app = wx.App(False)
# win = MainWindow(None)
# app.MainLoop()
