'''
Created on Dec 23, 2013

@author: Chris
'''

import wx
import sys
import Queue
import threading
from model.i18n import I18N

class MessagePump(object):
	def __init__(self, queue):
		self.queue = queue
		self.stdout = sys.stdout
	
	# Overrides stdout's write method
	def write(self, text):
		if text != '':
			self.queue.put(text)
		

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

class RuntimeDisplay(wx.Panel):
	def __init__(self, parent, **kwargs):
		wx.Panel.__init__(self, parent, **kwargs)
		
		self._translator = I18N()
		
		self._init_properties()
		self._init_components()
		self._do_layout()
		
		self.queue = Queue.Queue()
		_stdout = sys.stdout
		sys.stdout = MessagePump(self.queue)
		listener = Listener(self.queue, self.cmd_textbox)
		listener.start()

	def _init_properties(self):
		self.SetBackgroundColour('#F0F0F0')

	def _init_components(self):
		self.text = wx.StaticText(self, label=self._translator["status"])
		self.cmd_textbox = wx.TextCtrl(
										self, -1, "",
										style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH)
		
	def _do_layout(self):
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.AddSpacer(10)
		sizer.Add(self.text, 0, wx.LEFT, 30)
		sizer.AddSpacer(10)
		sizer.Add(self.cmd_textbox, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 30)
		sizer.AddSpacer(20)
		self.SetSizer(sizer)
		