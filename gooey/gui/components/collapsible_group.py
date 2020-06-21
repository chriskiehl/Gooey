import wx
from gooey.gui.util import wx_util
from gooey.gui.components.util.wrapped_static_text import AutoWrappedStaticText

class CollapsibleGroup(wx.CollapsiblePane):
    def __init__(self, parent, groupName, groupDescription, showBorders, showUnderline, labelColor, descriptionColor, groupTopMargin):
        super(CollapsibleGroup, self).__init__(parent, style=wx.CP_NO_TLW_RESIZE, label=groupName)
        # In order to be visible even when collapsed, the group name must be but in the CollapsiblePane's label.
        # To be consistant with the OptionGroups widget, h1 styling must be applied to the label,
        #  and the only way is to apply it to the whole wx.CollapsiblePane.
        # Widgets inherit the styles, so it means all childs would be h1.
        # To avoid redefining each child separately, an intermediate Pannel is created and defined as h2 (default style).
        # This intermediate Pannel is the one exposed in the interface so that children can inherit a proper type.
        fontSize = self.GetFont().GetPointSize()
        h1Font = wx.Font(fontSize * 1.2, *wx_util.styles['h1'])  # Equivalent to the StaticTexts created with h1().
        h2Font = wx.Font(fontSize, *wx_util.styles['h2'])  # Equivalent to the StaticTexts created with h2().
        self.SetFont(h1Font)
        self.SetForegroundColour(labelColor)
        if showBorders:
            boxDetails = wx.StaticBox(self.GetPane(), -1, groupName)
            self.firstLevelsizer = wx.StaticBoxSizer(boxDetails, wx.VERTICAL)
        else:
            self.firstLevelsizer = wx.BoxSizer(wx.VERTICAL)
            self.firstLevelsizer.AddSpacer(10)
        self.GetPane().SetSizer(self.firstLevelsizer)
        
        self.intermediateWindow = wx.Panel(self.GetPane())
        self.intermediateWindow.SetFont(h2Font)
        self.firstLevelsizer.Add(self.intermediateWindow, 0, wx.EXPAND | wx.LEFT, groupTopMargin)
        self.secondLevelSizer = wx.BoxSizer(wx.VERTICAL)
        self.intermediateWindow.SetSizer(self.secondLevelSizer)

        # Invariant : getSizerForChilds() and getParentForChilds() produce valid results.

        if groupDescription:
            description = AutoWrappedStaticText(self.getParentForChilds(), label=groupDescription, target=self.getSizerForChilds())
            description.SetForegroundColour(descriptionColor)
            description.SetFont(h2Font)
            self.getSizerForChilds().Add(description, 0,  wx.EXPAND | wx.LEFT, 10)

        if not showBorders and groupName and showUnderline:
            self.getSizerForChilds().Add(wx_util.horizontal_rule(self.getParentForChilds()), 0, wx.EXPAND | wx.LEFT, 10)

        self.Bind(wx.EVT_COLLAPSIBLEPANE_CHANGED, self.on_change)

    def on_change(self, event):
        self.GetParent().Layout()

    def getSizerForParent(self):
        """
        Returns the sizer which should be added to the higher level sizer.
        """
        return self.firstLevelsizer

    def getParentForChilds(self):
        """
        Returns the sizer to which the child widgets should be added.
        """
        return self.intermediateWindow

    def getSizerForChilds(self):
        return self.secondLevelSizer
