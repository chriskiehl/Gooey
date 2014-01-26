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

		self._init_components()
		self._do_layout()
		
	def _init_components(self):
		self.cancel_button = self._Button('Cancel', wx.ID_CANCEL)
		self.start_button = self._Button("Start", wx.ID_OK)
		self.cancel_run_button = self._Button('Cancel', wx.ID_CANCEL)
		
	def _do_layout(self):
		v_sizer = wx.BoxSizer(wx.VERTICAL)
		h_sizer = wx.BoxSizer(wx.HORIZONTAL)
		
		h_sizer.AddStretchSpacer(1)
		h_sizer.Add(self.cancel_button, 0, wx.ALIGN_RIGHT | wx.RIGHT, 20)
		h_sizer.Add(self.start_button, 0, wx.ALIGN_RIGHT | wx.RIGHT, 20)
		
		v_sizer.AddStretchSpacer(1)
		v_sizer.Add(h_sizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND)
		v_sizer.Add(self.cancel_run_button, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.RIGHT, 20)
		self.cancel_run_button.Hide()
		v_sizer.AddStretchSpacer(1)
		self.SetSizer(v_sizer)
		
	def _Button(self,label=None, style=None):
		return wx.Button(
				parent=self,
				id=-1,
				size=(90, 24),
				label=label,
				style=style)

	def RegisterController(self, controller):
		if self._controller is None: 
			self._controller = controller
			
	def NextPage(self):
		self.cancel_button.Hide()
		self.start_button.Hide() 
		self.cancel_run_button.Show()
		self.Layout()


class Footer(AbstractFooter):
	'''
	Footer section used on the configuration 
	screen of the application
	
	args:
		parent: wxPython parent window
		controller: controller class used in delagating all the commands
	'''
	
	def __init__(self, parent, controller, **kwargs):
		AbstractFooter.__init__(self, parent, **kwargs)
		
		self.Bind(wx.EVT_BUTTON, self.OnCancelButton, self.cancel_button)
		self.Bind(wx.EVT_BUTTON, self.OnStartButton, self.start_button)
		self.Bind(wx.EVT_BUTTON, self.OnCancelRunButton, self.cancel_run_button)
		
	def OnCancelButton(self, event):
		self._controller.OnCancelButton(event)
		event.Skip()
		
	def OnCancelRunButton(self, event):
		self._controller.OnCancelRunButton(event)
		event.Skip()
		
	def OnStartButton(self, event):
		self._controller.OnStartButton(event)
		event.Skip()


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
		
		self.start_button = None
		
		self.Bind(wx.EVT_BUTTON, self.OnMainCancel, self.cancel_button)
	
	def OnMainCancel(self, event):
		self._controller.OnMainCancel(event)
# 		event.Skip()
		
		
		
		
		