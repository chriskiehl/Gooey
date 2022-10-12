import wx  # type: ignore

class BasicTextConsole(wx.TextCtrl):
    def __init__(self, parent):
        super().__init__(parent, -1, "", style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH | wx.TE_AUTO_URL )
