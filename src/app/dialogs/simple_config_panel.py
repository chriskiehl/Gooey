'''
Created on Dec 9, 2013

@author: Chris


'''

import wx
import os

class BodyDisplayPanel(wx.Panel):
	def __init__(self, parent, **kwargs):
		wx.Panel.__init__(self, parent, **kwargs)

		self.SetBackgroundColour('#F0F0F0')
	
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.AddSpacer(10)
		
# 		about_header = wx.StaticText(self, label="About")
# 		about_header = self._bold_static_text("About")
# 		about_body = wx.StaticText(self, label="This program does bla. Enter the command line args of your choice to control bla and bla.")
# 		
# 		sizer.Add(about_header, 0, wx.LEFT | wx.RIGHT, 20)
# 		sizer.AddSpacer(5)
# 		sizer.Add(about_body, 0, wx.LEFT | wx.RIGHT, 20)
		
		sizer.AddSpacer(40)
		
		text = self._bold_static_text("Enter Command Line Arguments")
# 		
		sizer.Add(text, 0, wx.LEFT, 20)
		sizer.AddSpacer(10)
		
		h_sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.cmd_textbox = wx.TextCtrl(
							self, -1, "")
		h_sizer.Add(self.cmd_textbox, 1, wx.ALL | wx.EXPAND)
		sizer.Add(h_sizer, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 20)
		
		self.SetSizer(sizer)
		
	def get_contents(self):
		return self.cmd_textbox.GetValue()
		
	def _bold_static_text(self, text_label):
		bold = wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
		text = wx.StaticText(self, label=text_label)
		text.SetFont(bold)
		return text
	
		
		
