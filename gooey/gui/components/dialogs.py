import rewx.components as c  # type: ignore
import wx  # type: ignore
import wx.html2  # type: ignore
from rewx import wsx, render  # type: ignore


def _html_window(html):
    return wsx(
        [c.Block, {'orient': wx.VERTICAL, 'flag': wx.EXPAND},
         [c.HtmlWindow, {'style': wx.TE_READONLY, 'flag': wx.EXPAND | wx.ALL,
                         'proportion': 1, 'value': html}]]
    )


class HtmlDialog(wx.Dialog):
    """
    A MessageDialog where the central contents are an HTML window
    customizable by the user.
    """
    def __init__(self, *args, **kwargs):
        caption = kwargs.pop('caption', '')
        html = kwargs.pop('html', '')
        super(HtmlDialog, self).__init__(None, *args, **kwargs)

        wx.InitAllImageHandlers()

        self.SetTitle(caption)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(render(_html_window(html), self), 1, wx.EXPAND)

        # in addition to creating the sizer, this actually attached
        # a few common handlers which makes it feel more dialog-y. Thus
        # it being done here rather than in rewx
        btnSizer = self.CreateStdDialogButtonSizer(wx.OK)
        sizer.Add(btnSizer, 0, wx.ALL | wx.EXPAND, 9)
        self.SetSizer(sizer)
        self.Layout()



