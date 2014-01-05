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
		self.Add


		
	def AddRequiredArgsHeaderMsg(self):
		required_msg = wx.StaticText(self, label="Required Arguments")
		self.container.Add(required_msg, 0, wx.LEFT | wx.RIGHT, 20) 
		
	def AddWidgets(self, actions, widget_type):
		if len(actions) == 0: 
			return
		action = actions.pop(0)
		self.CreateHelpMsgWidget(action)
		if self.hasNargs(action):
			self.AddNargsMsg(action)
		self.AddWidget(widget_type)
		self.AddWidgets(actions, widget_type)
		
	def CreateHelpMsgWidget(self, action):
		help_msg = action.help 
		return wx.StaticText(self, label=help_msg)
	
	def HasNargs(self, action):
		return action.nargs > 0
	
	def AddNargsMsg(self, action):
		msg = action.nargs 
		return wx.StaticText(self, label=msg)
	
	def AddWidget(self, _type):
		widget = getattr(wx, _type)
		
			
if __name__ == '__main__':
	a = getattr(wx, 'StaticText')
	print a 
	
 
			
		
		
		
		
		
