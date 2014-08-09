'''
Created on Dec 9, 2013

@author: Chris
'''


import wx

from gooey.gui.option_reader import OptionReader
from gooey import i18n

class BasicConfigPanel(wx.Panel, OptionReader):
  def __init__(self, parent, params, **kwargs):
    wx.Panel.__init__(self, parent, **kwargs)

    self._translator = I18N(params['language'])

    self._init_properties()
    self._init_components()
    self._do_layout()

  def _init_components(self):
    self.header_msg = self._bold_static_text(self._translator['simple_config'])
    self.cmd_textbox = wx.TextCtrl(self, -1, "")

  def _init_properties(self):
    self.SetBackgroundColour('#F0F0F0')

  def _do_layout(self):
    sizer = wx.BoxSizer(wx.VERTICAL)
    sizer.AddSpacer(50)
    sizer.Add(self.header_msg, 0, wx.LEFT, 20)
    sizer.AddSpacer(10)
    h_sizer = wx.BoxSizer(wx.HORIZONTAL)
    h_sizer.Add(self.cmd_textbox, 1, wx.ALL | wx.EXPAND)
    sizer.Add(h_sizer, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 20)
    self.SetSizer(sizer)

  def _bold_static_text(self, text_label):
    text = wx.StaticText(self, label=text_label)
    font_size = text.GetFont().GetPointSize()
    bold = wx.Font(font_size, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
    text.SetFont(bold)
    return text

  def GetOptions(self):
    return self.cmd_textbox.GetValue()

  def RegisterController(self, controller):
    pass
	
		
		
