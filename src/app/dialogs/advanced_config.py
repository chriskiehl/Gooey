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
from app.dialogs.option_reader import OptionReader

PADDING = 10


class AdvancedConfigPanel(ScrolledPanel, OptionReader):
	'''
	Abstract class for the Footer panels. 
	'''
	def __init__(self, parent, parser, **kwargs):
		ScrolledPanel.__init__(self, parent, **kwargs)
		self.SetupScrolling()
		
		self.components = ComponentFactory(parser)
		
		self._controller = None
		
		self._init_components()
		self._do_layout()
		self.Bind(wx.EVT_SIZE, self.OnResize)

		
	def _init_components(self):
		self._msg_req_args = self.BuildHeaderMsg("Required Arguments")
		self._msg_opt_args = self.BuildHeaderMsg("Optional Arguments")
		
	def _do_layout(self):
		STD_LAYOUT = (0, wx.LEFT | wx.RIGHT | wx.EXPAND, PADDING)
		container = wx.BoxSizer(wx.VERTICAL)
		container.AddSpacer(15)
		
		container.Add(self._msg_req_args, 0, wx.LEFT | wx.RIGHT, PADDING)
		container.AddSpacer(5)
		container.Add(self._draw_horizontal_line(), *STD_LAYOUT)
		container.AddSpacer(20)
		
		self.AddWidgets(container, self.components.required_args, add_space=True)
		
		container.AddSpacer(10)
		
		container.AddSpacer(10)
		container.Add(self._msg_opt_args, 0, wx.LEFT | wx.RIGHT, PADDING)
		container.AddSpacer(5)
		container.Add(self._draw_horizontal_line(), *STD_LAYOUT)
		container.AddSpacer(20)
		
		flag_grids = self.CreateComponentGrid(self.components.flags, cols=3, vgap=15)	
		general_opts_grid = self.CreateComponentGrid(self.components.general_options) 
		container.Add(general_opts_grid, *STD_LAYOUT)
		container.AddSpacer(30)
		container.Add(flag_grids, *STD_LAYOUT)
		
		self.SetSizer(container)

	def BuildHeaderMsg(self, label):
		_msg = wx.StaticText(self, label=label)
		font_size = _msg.GetFont().GetPointSize()
		bold = wx.Font(font_size*1.2, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
		_msg.SetFont(bold)
		return _msg
		
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
		print 'SIZEEEE:', evt.m_size
		for component in self.components:
			component.Update(evt.m_size)
		evt.Skip()
	
	def RegisterController(self, controller):
		if self._controller is None:
			self._controller = controller
			
	def GetOptions(self):
		''' 
		returns the collective values from all of the
		widgets contained in the panel'''
		values = [(c._action, c.GetValue())
							for c in self.components]
		for i in values:
			print (i[0].option_strings[-1], i[-1])
		
		
		
			
if __name__ == '__main__':
	pass
 
			
		
		
		
		
		
