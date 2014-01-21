'''
Created on Dec 23, 2013

@author: Chris
'''

import wx

class AbstractFooter(wx.Panel):
	'''
	Abstract class for the Footer panels. 
	'''
	def __init__(self, parent, **kwargs):
		wx.Panel.__init__(self, parent, **kwargs)
		self.SetMinSize((30, 53))
		
		self._controller = None
		
		self.cancel_button = self._button('Cancel', wx.ID_CANCEL)
		self.next_button = self._button("Next", wx.ID_OK)
		
		self._do_layout()
		
	def _do_layout(self):
		v_sizer = wx.BoxSizer(wx.VERTICAL)
		h_sizer = wx.BoxSizer(wx.HORIZONTAL)
		
		h_sizer.AddStretchSpacer(1)
		h_sizer.Add(self.cancel_button, 0, wx.ALIGN_RIGHT | wx.RIGHT, 20)
		h_sizer.Add(self.next_button, 0, wx.ALIGN_RIGHT | wx.RIGHT, 20)
		
		v_sizer.AddStretchSpacer(1)
		v_sizer.Add(h_sizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND)
		v_sizer.AddStretchSpacer(1)
		self.SetSizer(v_sizer)
		
	def _button(self,label=None, style=None):
		return wx.Button(
				parent=self,
				id=-1,
				size=(90, 24),
				label=label,
				style=style)

	def RegisterController(self, controller):
		if self._controller is None: 
			self._controller = controller


class ConfigFooter(AbstractFooter):
	'''
	Footer section used on the configuration 
	screen of the application
	
	args:
		parent: wxPython parent window
		controller: controller class used in delagating all the commands
	'''
	
	def __init__(self, parent, controller, **kwargs):
		AbstractFooter.__init__(self, parent, **kwargs)
		
		self.Bind(wx.EVT_BUTTON, self.OnConfigCancel, self.cancel_button)
		self.Bind(wx.EVT_BUTTON, self.OnConfigNext, self.next_button)
		
	def OnConfigCancel(self, event):
		self._controller.OnConfigCancel(event)
		
	def OnConfigNext(self, event):
		self._controller.OnConfigNext(event)


class MainFooter(AbstractFooter):
	'''
	Footer section used on the Main Status  
	screen of the application
	
	args:
		parent: wxPython parent window
		controller: controller class used in delagating all the commands
	'''
	def __init__(self, parent, controller, **kwargs):
		AbstractFooter.__init__(self, parent, **kwargs)
		
		self.Bind(wx.EVT_BUTTON, self.OnConfigCancel, self.cancel_button)
		self.Bind(wx.EVT_BUTTON, self.OnConfigNext, self.next_button)
	
	def OnMainCancel(self, event):
		self._controller.OnMainCancel(event)
		
	def OnMainNext(self, event):
		self._controller.OnMainNext(event)
		
		
		
		
		
		