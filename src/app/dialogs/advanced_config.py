'''
Created on Dec 28, 2013

@author: Chris
'''

import wx
from wx.lib.scrolledpanel import ScrolledPanel


class AdvancedConfigPanel(ScrolledPanel):
	'''
	Abstract class for the Footer panels. 
	'''
	def __init__(self, parent, **kwargs):
		ScrolledPanel.__init__(self, parent, **kwargs)
		self.SetupScrolling()
		
		self.components = []
		
		self.container = wx.BoxSizer(wx.VERTICAL)
		self.container.AddSpacer(10)
		self.AddRequiredArgsHeaderMsg()


		
	def AddRequiredArgsHeaderMsg(self):
		required_msg = wx.StaticText(self, label="Required Arguments")
		self.container.Add(required_msg, 0, wx.LEFT | wx.RIGHT, 20) 
		
	def AddRequiredWidgets(self, factory):
		widgets = factory._positionals 
		for widget in widgets:
			
	
	
 
			
		
		
		
		
		
