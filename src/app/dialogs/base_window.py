'''
Created on Jan 19, 2014

New plan: 

	fuck the multi-component thing. 
	
	Bind and unbind the buttons on the panels. 

@author: Chris
'''

import os 
import sys
import wx
import header
import footer
from app.dialogs.runtime_display_panel import RuntimeDisplay
from app.dialogs.controller import Controller
from app.images import image_store
from app.dialogs.config_model import ConfigModel
from model.i18n import I18N

class BaseWindow(wx.Frame):

	def __init__(self, BodyPanel, model, payload, params):
		wx.Frame.__init__(
				self, 
				parent=None, 
				id=-1, 
				title=os.path.basename(__file__),
				size=(610,530)
		)
		
		self._params = params
		self._model = model
		self._payload = payload
		
		self._controller = None
		
		self._translator = I18N(params['language'])
		
		self._init_properties()
		self._init_components(BodyPanel)
		self._do_layout()
		self._init_controller()
		self.registerControllers()
		
	def _init_properties(self):
		self.SetMinSize((400,300))
		self.icon = wx.Icon(image_store.icon, wx.BITMAP_TYPE_ICO)
		self.SetIcon(self.icon)
		
	def _init_components(self, BodyPanel):
		# init components		
		self.head_panel = header.FrameHeader(
																	heading=self._translator["settings_title"], 
																	subheading = self._model.description,
																	parent=self, 
																	translator=self._translator)
		self.config_panel = BodyPanel(self)
		self.runtime_display = RuntimeDisplay(self)
		self.foot_panel = footer.Footer(self, self._controller, self._translator)
		
		self.panels = [self.head_panel, self.config_panel, self.foot_panel]
		
	def _do_layout(self):
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(self.head_panel, 0, wx.EXPAND)
		self._draw_horizontal_line(sizer)
		sizer.Add(self.config_panel, 1, wx.EXPAND)
		self.runtime_display.Hide()
		sizer.Add(self.runtime_display, 1, wx.EXPAND)
		self._draw_horizontal_line(sizer)
		sizer.Add(self.foot_panel, 0, wx.EXPAND)
		self.SetSizer(sizer)
		
	def _draw_horizontal_line(self, sizer):
		line = wx.StaticLine(self, -1, style=wx.LI_HORIZONTAL)
		line.SetSize((10, 10))
		sizer.Add(line, 0, wx.EXPAND)
	
	def _init_controller(self):
		self._controller = Controller(
															base_frame	 = self,
															head_panel	 = self.head_panel, 
															body_panel	 = self.config_panel, 
															footer_panel = self.foot_panel,
															model 			 = self._model,
															translator	 = self._translator)	
		
	def registerControllers(self):
		for panel in self.panels:
			panel.RegisterController(self._controller)
			
	def NextPage(self):
		self.head_panel.NextPage()
		self.foot_panel.NextPage()
		self.config_panel.Hide()
		self.runtime_display.Show() 
		self.Layout()
			
	def AttachPayload(self, payload):
		self._payload = payload
			
# 	def OnXClose(self, event):
# 		print 'adsfasdfadsf'
			

if __name__ == '__main__':
	pass