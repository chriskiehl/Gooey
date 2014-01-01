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
		self.SetMinSize((30, 50))
		
		self.cancel_button = self._button('Cancel', wx.ID_CANCEL)
		self.next_button = self._button("Next", wx.ID_OK)

		sizer = wx.BoxSizer(wx.HORIZONTAL)
		sizer.AddStretchSpacer(1)
		sizer.Add(self.cancel_button, 0, wx.ALIGN_RIGHT | wx.RIGHT | wx.TOP, 20)
		sizer.Add(self.next_button, 0, wx.ALIGN_RIGHT | wx.RIGHT | wx.TOP, 20)
		self.SetSizer(sizer)
		
	def _button(self,label=None, style=None):
		return wx.Button(
				parent=self,
				id=-1,
				size=(75, 23),
				label=label,
				style=style)


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
		
		self._controller = controller 
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
		
		self._controller = controller

		self.Bind(wx.EVT_BUTTON, self.OnConfigCancel, self.cancel_button)
		self.Bind(wx.EVT_BUTTON, self.OnConfigNext, self.next_button)
	
	def OnMainCancel(self, event):
		self._controller.OnMainCancel(event)
		
	def OnMainNext(self, event):
		self._controller.OnMainNext(event)