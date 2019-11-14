import wx
from gooey.gui.util import wx_util
from gooey.gui.components.util.wrapped_static_text import AutoWrappedStaticText

class OptionsGroup:
    def __init__(self, parent, groupName, groupDescription, showBorders, showUnderline, labelColor, descriptionColor, groupTopMargin):
        # determine the type of border , if any, the main sizer will use
        self.parent = parent
        if showBorders:
            boxDetails = wx.StaticBox(parent, -1, groupName)
            self.sizer = wx.StaticBoxSizer(boxDetails, wx.VERTICAL)
        else:
            self.sizer = wx.BoxSizer(wx.VERTICAL)
            self.sizer.AddSpacer(10)
            if groupName:
                groupNameWidget = wx_util.h1(parent, groupName)
                groupNameWidget.SetForegroundColour(labelColor)
                self.sizer.Add(groupNameWidget, 0, wx.TOP | wx.BOTTOM | wx.LEFT, 8)

        # Invariant : getSizerForChilds() and getParentForChilds() produce valid results.
        
        if groupDescription:
            description = AutoWrappedStaticText(self.getParentForChilds(), label=groupDescription, target=self.getSizerForChilds())
            description.SetForegroundColour(descriptionColor)
            self.getSizerForChilds().Add(description, 1,  wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
        # apply an underline when a grouping border is not specified
        if not showBorders and groupName and showUnderline:
            self.getSizerForChilds().Add(wx_util.horizontal_rule(parent), 0, wx.EXPAND | wx.LEFT, 10)

        self.marginSizer = wx.BoxSizer(wx.VERTICAL)
        self.marginSizer.Add(self.sizer, 1, wx.EXPAND | wx.TOP, groupTopMargin)
    
    def getSizerForParent(self):
        """
        Returns the sizer which should be added to the higher level sizer.
        """
        return self.marginSizer

    def getSizerForChilds(self):
        """
        Returns the sizer to which the child widgets should be added.
        """
        return self.sizer

    def getParentForChilds(self):
        return self.parent
