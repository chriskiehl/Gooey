'''
Created on Dec 28, 2013

@author: Chris
'''
import os 
import wx 
from wx.lib import scrolledpanel
from app.dialogs.advanced_config import AdvancedConfigPanel

class MainWindow(wx.Frame):
					
	def __init__(self):
		wx.Frame.__init__(
			self, 
			parent=None, 
			id=-1, 
			title=os.path.basename(__file__),
			size=(640,480)
		)
		
		self._init_components()
		
	def _init_components(self):
		# init components		
		self.SetMinSize((400,300))
		
		panel = AdvancedConfigPanel(self)
		
		sizer = wx.BoxSizer(wx.VERTICAL)
		
# 		for i in range(40): 
# 			t = wx.TextCtrl(panel, -1)
# 			sizer.Add(t, 0)
			
		panel.SetSizer(sizer)
		
		_sizer = wx.BoxSizer(wx.VERTICAL)
		_sizer.Add(panel, 1, wx.EXPAND)
		self.SetSizer(_sizer)
		
	def _draw_horizontal_line(self):
		line = wx.StaticLine(self, -1, style=wx.LI_HORIZONTAL)
		line.SetSize((10, 10))
		self.sizer.Add(line, 0, wx.EXPAND)
		
if __name__ == '__main__':
	app = wx.App(False)  
	frame = MainWindow()
	frame.Show(True)     # Show the frame.
	app.MainLoop()