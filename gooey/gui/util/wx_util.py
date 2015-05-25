"""
Collection of Utility methods for creating pre-styled wxWidgets items
"""

__author__ = 'Chris'


import wx


def MakeBold(statictext):
  pointsize = statictext.GetFont().GetPointSize()
  font = wx.Font(pointsize, wx.FONTFAMILY_DEFAULT,
                 wx.FONTWEIGHT_NORMAL, wx.FONTWEIGHT_BOLD, False)
  statictext.SetFont(font)


def _bold_static_text(parent, text_label):
  text = wx.StaticText(parent, label=text_label)
  font_size = text.GetFont().GetPointSize()
  bold = wx.Font(font_size, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
  text.SetFont(bold)
  return text


def H1(parent, label):
  text = wx.StaticText(parent, label=label)
  font_size = text.GetFont().GetPointSize()
  font = wx.Font(font_size * 1.2, wx.FONTFAMILY_DEFAULT, wx.FONTWEIGHT_NORMAL, wx.FONTWEIGHT_BOLD, False)
  text.SetFont(font)
  return text

def H2(parent, label):
  text = wx.StaticText(parent, label=label)
  font_size = text.GetFont().GetPointSize()
  font = wx.Font(font_size * 1.2, wx.FONTFAMILY_DEFAULT, wx.FONTWEIGHT_NORMAL, wx.FONTWEIGHT_NORMAL, False)
  text.SetFont(font)
  return text

def HorizontalRule(parent):
  line = wx.StaticLine(parent, -1, style=wx.LI_HORIZONTAL)
  line.SetSize((10, 10))
  return line

def vertical_rule(parent):
  line = wx.StaticLine(parent, -1, style=wx.LI_VERTICAL)
  line.SetSize((10, 10))
  return line

def MakeDarkGrey(statictext):
  darkgray = (54, 54, 54)
  statictext.SetForegroundColour(darkgray)
