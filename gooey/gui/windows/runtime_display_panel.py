'''
Created on Dec 23, 2013

@author: Chris
'''

import sys

import wx

from gooey.gui.lang import i18n
from gooey.gui.message_event import EVT_MSG


class MessagePump(object):
  def __init__(self):
    # 		self.queue = queue
    self.stdout = sys.stdout

  # Overrides stdout's write method
  def write(self, text):
    raise NotImplementedError


class RuntimeDisplay(wx.Panel):
  def __init__(self, parent, build_spec, **kwargs):
    wx.Panel.__init__(self, parent, **kwargs)

    self.build_spec = build_spec

    self._init_properties()
    self._init_components()
    self._do_layout()
    # self._HookStdout()

  def _init_properties(self):
    self.SetBackgroundColour('#F0F0F0')

  def _init_components(self):
    self.text = wx.StaticText(self, label=i18n._("status"))
    self.cmd_textbox = wx.TextCtrl(
      self, -1, "",
      style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH)
    if self.build_spec.get('monospace_display'):
      pointsize = self.cmd_textbox.GetFont().GetPointSize()
      font = wx.Font(pointsize, wx.FONTFAMILY_MODERN,
                   wx.FONTWEIGHT_NORMAL, wx.FONTWEIGHT_BOLD, False)
      self.cmd_textbox.SetFont(font)

  def _do_layout(self):
    sizer = wx.BoxSizer(wx.VERTICAL)
    sizer.AddSpacer(10)
    sizer.Add(self.text, 0, wx.LEFT, 30)
    sizer.AddSpacer(10)
    sizer.Add(self.cmd_textbox, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 30)
    sizer.AddSpacer(20)
    self.SetSizer(sizer)

    self.Bind(EVT_MSG, self.OnMsg)

  def _HookStdout(self):
    _stdout = sys.stdout
    _stdout_write = _stdout.write

    sys.stdout = MessagePump()
    sys.stdout.write = self.WriteToDisplayBox

  def AppendText(self, txt):
    self.cmd_textbox.AppendText(txt)

  def WriteToDisplayBox(self, txt):
    if txt is not '':
      self.AppendText(txt)

  def OnMsg(self, evt):
    pass
