'''
Created on Dec 23, 2013

@author: Chris
'''

import wx

class BasicDisplayPanel(wx.Panel):
	def __init__(self, parent, **kwargs):
		wx.Panel.__init__(self, parent, **kwargs)

		self.SetBackgroundColour('#F0F0F0')

		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.AddSpacer(10)
		text = wx.StaticText(self, label="Running bla bla bla")
		sizer.Add(text, 0, wx.LEFT, 20)
		sizer.AddSpacer(10)

		self.cmd_textbox = wx.TextCtrl(
										self, -1, "",
										style=wx.TE_MULTILINE | wx.TE_READONLY)
		sizer.Add(self.cmd_textbox, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 20)
		self.SetSizer(sizer)
		