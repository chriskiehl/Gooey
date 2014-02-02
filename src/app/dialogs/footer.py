'''
Created on Dec 23, 2013

@author: Chris
'''

import wx
import wx.animate
import imageutil
from app.images import image_store

class AbstractFooter(wx.Panel):
	'''
	Abstract class for the Footer panels. 
	'''
	def __init__(self, parent, translator, **kwargs):
		wx.Panel.__init__(self, parent, **kwargs)
		self.SetMinSize((30, 53))
		
		self._controller = None
		
		self._translator = translator

		self._init_components()
		self._init_pages()
		self._do_layout()
		
		
	def _init_components(self):
		'''
		initialize all of the components used in the footer
		TODO: 
			Add Checkmark image for when the program has finished running. 
			Refactor image tools into their own module. The resize code is 
			getting spread around a bit. 
		'''
		self.cancel_button = self._Button(self._translator['cancel'], wx.ID_CANCEL)
		self.start_button = self._Button(self._translator['start'], wx.ID_OK)
		self.running_animation = wx.animate.GIFAnimationCtrl(self, -1, image_store.loader)
		self.close_button = self._Button(self._translator["close"], wx.ID_OK)
	
	def _init_pages(self):
		_pages = [[
						self.cancel_button.Hide,
						self.start_button.Hide, 
						self.running_animation.Show,
						self.running_animation.Play,
						self.Layout
						],
					[
						self.running_animation.Stop,
						self.running_animation.Hide,
						self.close_button.Show,
						self.Layout
					]]
		self._pages = iter(_pages)
		
	def _do_layout(self):
		v_sizer = wx.BoxSizer(wx.VERTICAL)
		h_sizer = wx.BoxSizer(wx.HORIZONTAL)
		
		h_sizer.AddStretchSpacer(1)
		h_sizer.Add(self.cancel_button, 0, wx.ALIGN_RIGHT | wx.RIGHT, 20)
		h_sizer.Add(self.start_button, 0, wx.ALIGN_RIGHT | wx.RIGHT, 20)
		
		v_sizer.AddStretchSpacer(1)
		v_sizer.Add(h_sizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND)
		v_sizer.Add(self.running_animation, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.RIGHT, 20)
		self.running_animation.Hide()
		v_sizer.Add(self.close_button, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.RIGHT, 20)
		self.close_button.Hide()
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
		page = next(self._pages)
		for action in page: 
			action()
		
	def _load_image(self, img_path, height=70):
		return imageutil._resize_bitmap(
										self, 
										imageutil._load_image(img_path),
										height)


class Footer(AbstractFooter):
	'''
	Footer section used on the configuration 
	screen of the application
	
	args:
		parent: wxPython parent window
		controller: controller class used in delagating all the commands
	'''
	
	def __init__(self, parent, controller, translator, **kwargs):
		AbstractFooter.__init__(self, parent, translator, **kwargs)
		
		self.Bind(wx.EVT_BUTTON, self.OnCancelButton, self.cancel_button)
		self.Bind(wx.EVT_BUTTON, self.OnStartButton, self.start_button)
		self.Bind(wx.EVT_BUTTON, self.OnCloseButton, self.close_button)
		
	def OnCancelButton(self, event):
		self._controller.OnCancelButton(event)
		event.Skip()
		
	def OnCloseButton(self, event):
		self._controller.OnCloseButton(event)
		event.Skip()
		
	def OnStartButton(self, event):
		self._controller.OnStartButton(event)
		event.Skip()



		
		
		
		