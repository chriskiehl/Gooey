'''
Created on Dec 8, 2013

@author: Chris
'''

import wx 
import os
import sys
import threading
from model.controller import Controller 
from app.images import image_store
from app.dialogs.header import FrameHeader
from app.dialogs.body import BodyDisplayPanel
from app.dialogs.footer import ConfigFooter 

class MessagePump(object):
	def __init__(self, queue):
		self.queue = queue
		self.stdout = sys.stdout
	
	# Overrides stdout's write method
	def write(self, text):
		if text != '':
			self.queue.put(text)
		

class MainWindow(wx.Frame):
					
	class Listener(threading.Thread):
		def __init__(self, queue, textbox):
			threading.Thread.__init__(self)
			self.queue = queue
			self.update_text = lambda x: textbox.AppendText(x)
			
		def run(self):
			while True:
				try:
					stdout_msg = self.queue.get(timeout=1)
					if stdout_msg != '':
						self.update_text(stdout_msg)
				except Exception as e:
					pass # Timeout. Aint nobody care 'bout dat 

	def __init__(self, queue, payload=None):
		wx.Frame.__init__(
			self, 
			parent=None, 
			id=-1, 
			title=os.path.basename(__file__),
			size=(640,480)
		)
		
		self._controller = Controller()
		
		self._frame_header = FrameHeader
		self._simple_config_body = None
		self._adv_config_body = None	
		self._config_footer = None 
		self._output_footer = None 
		
		self._init_components()
		
 		self.queue = queue
 		# the client's main function
 		self._payload = payload
		
		_stdout = sys.stdout
		sys.stdout = MessagePump(queue)
		listener = MainWindow.Listener(queue, self.panel2.cmd_textbox)
		listener.start()
		
	def _init_components(self):
		# init components		
		self.SetMinSize((400,300))
		self.icon = wx.Icon(image_store.icon, wx.BITMAP_TYPE_ICO)
		self.SetIcon(self.icon)
		
		panel1 = FrameHeader(image_path=image_store.computer3, parent=self, size=(30,90))

		self.sizer = wx.BoxSizer(wx.VERTICAL)
		self.sizer.Add(panel1, 0, wx.EXPAND)

		self._draw_horizontal_line()

		self.panel2 = BodyDisplayPanel(parent=self)
		self.sizer.Add(self.panel2, 1, wx.EXPAND)
		self.SetSizer(self.sizer)

		self._draw_horizontal_line()

		self.footer = ConfigFooter(self, self._controller)
		self.sizer.Add(self.footer, 0, wx.EXPAND)
		
	def _draw_horizontal_line(self):
		line = wx.StaticLine(self, -1, style=wx.LI_HORIZONTAL)
		line.SetSize((10, 10))
		self.sizer.Add(line, 0, wx.EXPAND)
		
		
		
		
		
		
		
		
		