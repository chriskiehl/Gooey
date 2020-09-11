"""
Collection of Utility methods for creating often used, pre-styled wx Widgets
"""

import wx
from contextlib import contextmanager

from gooey.gui.three_to_four import Constants


@contextmanager
def transactUI(obj):
    """
    Coarse grain UI locking to avoid glitchy UI updates
    """
    obj.Freeze()
    try:
        yield
    finally:
        obj.Layout()
        obj.Thaw()




styles = {
    'h0': (wx.FONTFAMILY_DEFAULT, Constants.WX_FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False),
    'h1': (wx.FONTFAMILY_DEFAULT, Constants.WX_FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False),
    'h2': (wx.FONTFAMILY_DEFAULT, Constants.WX_FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False),
    'bold': (wx.FONTFAMILY_DEFAULT, Constants.WX_FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False)
}




def make_bold(statictext):
    pointsize = statictext.GetFont().GetPointSize()
    font = wx.Font(pointsize, *styles['bold'])
    statictext.SetFont(font)


def dark_grey(statictext):
    return withColor(statictext, (54, 54, 54))


def withColor(statictext, hex):
    statictext.SetForegroundColour(hex)
    return statictext


def h0(parent, label):
    text = wx.StaticText(parent, label=label)
    font_size = text.GetFont().GetPointSize()
    font = wx.Font(int(font_size * 1.4, *styles['h0']))
    text.SetFont(font)
    return text


def h1(parent, label):
    return _header(parent, label, styles['h1'])


def h2(parent, label):
    return _header(parent, label, styles['h2'])


def _header(parent, label, styles):
    text = wx.StaticText(parent, label=label)
    font_size = text.GetFont().GetPointSize()
    font = wx.Font(int(font_size * 1.2), *styles)
    text.SetFont(font)
    return text


def horizontal_rule(parent):
    return _rule(parent, wx.LI_HORIZONTAL)


def vertical_rule(parent):
    return _rule(parent, wx.LI_VERTICAL)


def _rule(parent, direction):
    line = wx.StaticLine(parent, -1, style=direction)
    line.SetSize((10, 10))
    return line
