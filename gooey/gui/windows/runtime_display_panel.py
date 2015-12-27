'''
Created on Dec 23, 2013

@author: Chris
'''

import wx
from gooey.gui.lang import i18n


class RuntimeDisplay(wx.Panel):
  '''
  Textbox displayed during the client program's execution.
  '''
  def __init__(self, parent, **kwargs):
    wx.Panel.__init__(self, parent, **kwargs)
    self._init_properties()
    self._init_components()
    self._do_layout()


  def set_font_style(self, style):
    pointsize = self.cmd_textbox.GetFont().GetPointSize()
    font = wx.Font(pointsize, style,
                 wx.FONTWEIGHT_NORMAL, wx.FONTWEIGHT_BOLD, False)
    self.cmd_textbox.SetFont(font)

  def _init_properties(self):
    self.SetBackgroundColour('#F0F0F0')

  def _init_components(self):
    self.text = wx.StaticText(self, label=i18n._("status"))

    self.cmd_textbox = wx.TextCtrl(
      self, -1, "",
      style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH)


  def _do_layout(self):
    sizer = wx.BoxSizer(wx.VERTICAL)
    sizer.AddSpacer(10)
    sizer.Add(self.text, 0, wx.LEFT, 30)
    sizer.AddSpacer(10)
    sizer.Add(self.cmd_textbox, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 30)
    sizer.AddSpacer(20)
    self.SetSizer(sizer)

  def append_text(self, txt):
    self.cmd_textbox.AppendText(txt)

