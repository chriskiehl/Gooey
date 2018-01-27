import wx

from gooey.gui.lang import i18n


class Console(wx.Panel):
    '''
    Textbox console/terminal displayed during the client program's execution.
    '''

    def __init__(self, parent, buildSpec, **kwargs):
        wx.Panel.__init__(self, parent, **kwargs)
        self.buildSpec = buildSpec

        self.text = wx.StaticText(self, label=i18n._("status"))
        self.textbox = wx.TextCtrl(
            self, -1, "", style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH
        )

        self.defaultFont = self.textbox.GetFont()

        self.textbox.SetFont(wx.Font(
            self.buildSpec['terminal_font_size'] or self.defaultFont.GetPointSize(),
            self.getFontStyle(),
            wx.NORMAL,
            self.buildSpec['terminal_font_weight'] or wx.NORMAL,
            False,
            self.getFontFace(),
        ))
        self.textbox.SetForegroundColour(self.buildSpec['terminal_font_color'])
         
        self.layoutComponent()
        self.Layout()


    def getFontStyle(self):
        """
        Force wx.Modern style to support legacy
        monospace_display param when present
        """
        return (wx.MODERN
                if self.buildSpec['monospace_display']
                else wx.DEFAULT)


    def getFontFace(self):
        """Choose the best font face available given the user options"""
        userFace = self.buildSpec['terminal_font_family'] or self.defaultFont.GetFaceName()
        return (''
                if self.buildSpec['monospace_display']
                else userFace)


    def logOutput(self, *args, **kwargs):
        """Event Handler for console updates coming from the client's program"""
        self.appendText(kwargs.get('msg'))


    def appendText(self, txt):
        """
        Append the text to the main TextCtrl.

        Note! Must be called from a Wx specific thread handler to avoid
        multi-threaded explosions (e.g. wx.CallAfter)
        """
        self.textbox.AppendText(txt)


    def getText(self):
        return self.textbox.GetValue()

    def layoutComponent(self):
        self.SetBackgroundColour(self.buildSpec.get('terminal_bg_color', '#F0F0F0'))
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.AddSpacer(10)
        sizer.Add(self.text, 0, wx.LEFT, 20)
        sizer.AddSpacer(10)
        sizer.Add(self.textbox, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 20)
        sizer.AddSpacer(20)
        self.SetSizer(sizer)


