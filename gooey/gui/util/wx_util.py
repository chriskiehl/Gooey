"""
Collection of Utility methods for creating often used, pre-styled wx Widgets
"""

import wx


def make_bold(statictext):
  pointsize = statictext.GetFont().GetPointSize()
  font = wx.Font(pointsize, wx.FONTFAMILY_DEFAULT,
                 wx.FONTWEIGHT_NORMAL, wx.FONTWEIGHT_BOLD, False)
  statictext.SetFont(font)

def dark_grey(statictext):
  darkgray = (54, 54, 54)
  statictext.SetForegroundColour(darkgray)

def h0(parent, label):
  text = wx.StaticText(parent, label=label)
  font_size = text.GetFont().GetPointSize()
  font = wx.Font(font_size * 1.4, *(wx.FONTFAMILY_DEFAULT, wx.FONTWEIGHT_NORMAL, wx.FONTWEIGHT_BOLD, False))
  text.SetFont(font)
  return text

def h1(parent, label):
  return _header(parent, label, (wx.FONTFAMILY_DEFAULT, wx.FONTWEIGHT_NORMAL, wx.FONTWEIGHT_BOLD, False))

def h2(parent, label):
  return _header(parent, label, (wx.FONTFAMILY_DEFAULT, wx.FONTWEIGHT_NORMAL, wx.FONTWEIGHT_NORMAL, False))

def _header(parent, label, styles):
  text = wx.StaticText(parent, label=label)
  font_size = text.GetFont().GetPointSize()
  font = wx.Font(font_size * 1.2, *styles)
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


