import wx

from gooey.gui.util import wx_util


class Sidebar(wx.Panel):
    """
    Sidebar handles the show/hide logic so that it mirrors the functionality
    of the wx.Notebook class (which wants to control everything)
    """
    def __init__(self, parent, buildSpec, configPanels, *args, **kwargs):
        super(Sidebar, self).__init__(parent, *args, **kwargs)
        self._parent = parent
        self.buildSpec = buildSpec
        self.configPanels = configPanels
        self.activeSelection = 0
        self.options = list(self.buildSpec['widgets'].keys())
        self.leftPanel = wx.Panel(self)
        self.label = wx_util.h1(self.leftPanel, self.buildSpec.get('sidebar_title'))
        self.listbox = wx.ListBox(self.leftPanel, -1, choices=self.options)
        self.Bind(wx.EVT_LISTBOX, self.swapConfigPanels, self.listbox)
        self.layoutComponent()
        self.listbox.SetSelection(0)


    def getSelectedGroup(self):
        """Return the currently active 'group' i.e. the root SubParser """
        return self.options[self.activeSelection]


    def getActiveConfig(self):
        """Return the currently visible config screen"""
        return self.configPanels[self.activeSelection]


    def swapConfigPanels(self, event):
        """Hide/show configuration panels based on the currently selected
         option in the sidebar """
        for id, panel in enumerate(self.configPanels):
            panel.Hide()
        self.activeSelection = event.Selection
        self.configPanels[event.Selection].Show()
        self._parent.Layout()


    def layoutComponent(self):
        left = self.layoutLeftSide()

        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(left, 0, wx.EXPAND)

        if not self.buildSpec['tabbed_groups']:
            # only add it for non-tabbed layouts as it looks
            # weird against the tabbed ones
            hsizer.Add(wx_util.vertical_rule(self), 0, wx.EXPAND)

        for body in self.configPanels:
            body.Reparent(self)
            hsizer.Add(body, 1, wx.EXPAND)
            body.Hide()
        self.configPanels[0].Show()
        self.SetSizer(hsizer)

        if not self.buildSpec['show_sidebar']:
            left.Show(False)

        self.Layout()


    def layoutLeftSide(self):
        self.leftPanel.SetBackgroundColour(self.buildSpec['sidebar_bg_color'])
        self.leftPanel.SetSize((180, 0))
        self.leftPanel.SetMinSize((180, 0))

        container = wx.BoxSizer(wx.VERTICAL)
        container.AddSpacer(15)
        container.Add(self.label, 0, wx.LEFT | wx.RIGHT | wx.EXPAND, 10)
        container.AddSpacer(5)

        container.Add(self.listbox, 1, wx.LEFT | wx.RIGHT | wx.EXPAND, 10)
        container.AddSpacer(20)
        self.leftPanel.SetSizer(container)
        return self.leftPanel



