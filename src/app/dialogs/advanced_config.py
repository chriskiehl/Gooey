'''
Created on Dec 28, 2013

@author: Chris
'''

import wx
import components
from wx.lib import wordwrap
from itertools import chain
from component_factory import ComponentFactory
from wx.lib.scrolledpanel import ScrolledPanel

PADDING = 10


class AdvancedConfigPanel(ScrolledPanel):
	'''
	Abstract class for the Footer panels. 
	'''
	def __init__(self, parent, parser, **kwargs):
		ScrolledPanel.__init__(self, parent, **kwargs)
		self.SetupScrolling()
		
		self.components = ComponentFactory(parser)
		
		self.container = wx.BoxSizer(wx.VERTICAL)
		self.container.AddSpacer(15)
		
		self.AddHeaderMsg("Required Arguments")
		self.container.AddSpacer(10)
		
		box = wx.StaticBox(self, label="")
		boxsizer = wx.StaticBoxSizer(box, wx.VERTICAL)
		self.AddWidgets(self.container, self.components.positionals, add_space=True)
		
		self.container.AddSpacer(10)
		self.container.Add(self._draw_horizontal_line(), 
											0, wx.LEFT | wx.RIGHT | wx.EXPAND, PADDING)
		
		self.container.AddSpacer(10)
		self.AddHeaderMsg("Optional Arguments")
		self.container.AddSpacer(15)
		
		flag_grids = self.CreateComponentGrid(self.components.flags, vgap=15)	
		opt_choice_counter_grid = self.CreateComponentGrid(c for c in self.components 
																											if not isinstance(c, components.Flag)
																											and not isinstance(c, components.Positional)) 
		self.container.Add(opt_choice_counter_grid, 0, wx.LEFT | wx.RIGHT | wx.EXPAND, PADDING)
		self.container.AddSpacer(30)
		self.container.Add(flag_grids, 0, wx.LEFT | wx.RIGHT | wx.EXPAND, PADDING)
		
# 		sizer_params = [(grid, 0, wx.LEFT|wx.RIGHT|wx.EXPAND, PADDING)
# 										for grid in component_grids]
# 		self.container.AddMany(sizer_params) 
		self.SetSizer(self.container)
		self.Bind(wx.EVT_SIZE, self.OnResize)


	def AddHeaderMsg(self, label):
		required_msg = wx.StaticText(self, label=label)
		font_size = required_msg.GetFont().GetPointSize()
		bold = wx.Font(font_size*1.2, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
		required_msg.SetFont(bold)
		self.container.Add(required_msg, 0, wx.LEFT | wx.RIGHT, PADDING)
		 
		
	def AddWidgets(self, sizer, components, add_space=False, padding=PADDING):
		for component in components: 
			widget_group = component.Build(parent=self)
			sizer.Add(widget_group, 0, wx.LEFT | wx.RIGHT | wx.EXPAND, padding)
			if add_space:
				sizer.AddSpacer(8)
		
	def CreateComponentGrid(self, components, cols=2, vgap=10):
		gridsizer = wx.GridSizer(rows=0, cols=cols, vgap=vgap,hgap=4)
		self.AddWidgets(gridsizer, components)
		return gridsizer
		
	def _draw_horizontal_line(self):
		line = wx.StaticLine(self, -1, style=wx.LI_HORIZONTAL)
		line.SetSize((10, 10))
		return line
	
	def OnResize(self, evt):
		print evt.m_size
		for component in self.components:
			component.Update(evt.m_size)
		
		
			
if __name__ == '__main__':
	pass
 
			
		
		
		
		
		
