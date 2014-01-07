'''
Created on Dec 28, 2013

@author: Chris
'''

import wx
 
from component_factory import ComponentFactory
from wx.lib.scrolledpanel import ScrolledPanel




class AdvancedConfigPanel(ScrolledPanel):
	'''
	Abstract class for the Footer panels. 
	'''
	def __init__(self, parent, parser, **kwargs):
		ScrolledPanel.__init__(self, parent, **kwargs)
		self.SetupScrolling()
		
		self.components = ComponentFactory(parser)
		
		self.container = wx.BoxSizer(wx.VERTICAL)
		self.container.AddSpacer(10)
		
		self.AddRequiredArgsHeaderMsg()
		self.AddWidgets(self.components.positionals)
		
		self.SetSizer(self.container)


	def AddRequiredArgsHeaderMsg(self):
		required_msg = wx.StaticText(self, label="Required Arguments")
		self.container.Add(required_msg, 0, wx.LEFT | wx.RIGHT, 20) 
		
	def AddWidgets(self, components):
		if not components: 
			return 
		component = components[0]
		widget_group = component.Build(parent=self)
		self.container.Add(widget_group)
		self.AddWidgets(components[1:])
		
		
			
if __name__ == '__main__':
	pass
 
			
		
		
		
		
		
