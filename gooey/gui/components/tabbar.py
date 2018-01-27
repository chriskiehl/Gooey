import wx

from gooey.gui import events
from gooey.gui.pubsub import pub
from gooey.gui.util import wx_util


class Tabbar(wx.Panel):
    def __init__(self, parent, buildSpec, configPanels, *args, **kwargs):
        super(Tabbar, self).__init__(parent, *args, **kwargs)
        self._parent = parent
        self.notebook = wx.Notebook(self, style=wx.BK_DEFAULT)
        self.buildSpec = buildSpec
        self.configPanels = configPanels
        self.options = list(self.buildSpec['widgets'].keys())
        self.layoutComponent()


    def layoutComponent(self):
        for group, panel in zip(self.options, self.configPanels):
            panel.Reparent( self.notebook)
            self.notebook.AddPage(panel, group)
            self.notebook.Layout()

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.notebook, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.Layout()

    def getSelectedGroup(self):
        return self.options[self.notebook.Selection]

    def getActiveConfig(self):
        return self.configPanels[self.notebook.Selection]

    def show(self, b):
        self.Show(b)
