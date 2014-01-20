'''
Created on Jan 19, 2014

@author: Chris
'''

import os 
import wx
import header
import footer
from model.controller import Controller
from app.images import image_store

class BaseWindow(wx.Frame):

	def __init__(self, BodyPanel, parser):
		wx.Frame.__init__(
			self, 
			parent=None, 
			id=-1, 
			title=os.path.basename(__file__),
			size=(610,530)
		)
		
		self._parser = parser
		self._controller = Controller()
		
		self._init_properties()
		self._init_components(BodyPanel)
		self._do_layout()
		
	def _init_properties(self):
		self.SetMinSize((400,300))
		self.icon = wx.Icon(image_store.icon, wx.BITMAP_TYPE_ICO)
		self.SetIcon(self.icon)
		
	def _init_components(self, BodyPanel):
		# init components		
		self.head_panel = header.FrameHeader(
																	heading="Settings", 
																	subheading = self._parser.description,
																	image_path=image_store.settings2, 
																	parent=self, 
																	size=(30,90))
		self.body_panel = BodyPanel(self, self._parser)
		self.cfg_foot_panel = footer.ConfigFooter(self, self._controller)
# 		self.main_foot_panel = footer.MainFooter(self, self._controller)
# 		self.main_foot_panel.Hide()
		
	def _do_layout(self):
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(self.head_panel, 0, wx.EXPAND)
		self._draw_horizontal_line(sizer)
		sizer.Add(self.body_panel, 1, wx.EXPAND)
		self._draw_horizontal_line(sizer)
		sizer.Add(self.cfg_foot_panel, 0, wx.EXPAND)
		self.SetSizer(sizer)
		
# 	def _init_panels(self):
# 		self._frame_header = FrameHeader
# 		self._basic_config_body = None
# 		self._adv_config_body = None	
# 		self._config_footer = None 
# 		self._output_footer = None
		
	def _draw_horizontal_line(self, sizer):
		line = wx.StaticLine(self, -1, style=wx.LI_HORIZONTAL)
		line.SetSize((10, 10))
		sizer.Add(line, 0, wx.EXPAND)
		



if __name__ == '__main__':
	pass