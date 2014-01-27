'''
Created on Dec 23, 2013

@author: Chris
'''

import wx
import imageutil
from app.images import image_store

PAD_SIZE = 10

class FrameHeader(wx.Panel):
	
	def __init__(self,
				heading='',
				subheading='',
				image_path=None,
				dlg_style=1,
				**kwargs):

		wx.Panel.__init__(self, **kwargs)
		
		self._controller = None
		
		self._init_properties()
		self._init_components(heading, subheading, image_path)
		self._do_layout()
		

	def _init_properties(self):
		self.SetBackgroundColour('#ffffff')
		self.SetMinSize((120, 80))
		
	def _init_components(self, heading, subheading, image_path):
		self._header = self._bold_static_text(heading)
		self._subheader = wx.StaticText(self, label=subheading)
		self._settings_img = self._load_image(image_path)
		self._running_img = self._load_image(image_store.harwen_monitor)
		
	def _do_layout(self):
		vsizer = wx.BoxSizer(wx.VERTICAL)
		sizer = wx.BoxSizer(wx.HORIZONTAL)
		headings_sizer = self.build_heading_sizer()
		sizer.Add(headings_sizer, 1, wx.ALIGN_LEFT | wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND | wx.LEFT, PAD_SIZE)
		sizer.Add(self._settings_img, 0, wx.ALIGN_RIGHT | wx.EXPAND | wx.RIGHT, PAD_SIZE)
		sizer.Add(self._running_img, 0, wx.ALIGN_RIGHT | wx.EXPAND | wx.RIGHT, PAD_SIZE)
		self._running_img.Hide()
		vsizer.Add(sizer, 1, wx.EXPAND)
		self.SetSizer(vsizer)
		
	def _bold_static_text(self, label):
		txt = wx.StaticText(self, label=label)
		font_size = txt.GetFont().GetPointSize()
		txt.SetFont(wx.Font(font_size * 1.2, wx.FONTFAMILY_DEFAULT,
				wx.FONTWEIGHT_NORMAL, wx.FONTWEIGHT_BOLD, False)
		)
		return txt 

	def build_heading_sizer(self):
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.AddStretchSpacer(1)
		sizer.Add(self._header, 0)
		sizer.Add(self._subheader, 0)
		sizer.AddStretchSpacer(1)
		return sizer
	
	def _load_image(self, image_path):
		try:
			bitmap = wx.Bitmap(image_path)
			print bitmap
			bitmap = self._resize_bitmap(bitmap)
			return wx.StaticBitmap(self, -1, bitmap)
		except:
			raise IOError('Invalid Image path')
			
	def _resize_bitmap(self, bmap):
		'''
		Resizes a bitmap to a height of 89 pixels (the 
		size of the top panel), while keeping aspect ratio 
		in tact
		'''
		image = wx.ImageFromBitmap(bmap) 
		width, height = image.GetSize()
		ratio = float(width) / height
		target_height = 79 
		image = image.Scale(target_height * ratio, target_height,
				wx.IMAGE_QUALITY_HIGH
				)
		return wx.BitmapFromImage(image)

	def RegisterController(self, controller):
		if self._controller is None: 
			self._controller = controller
			
	def NextPage(self):
		self._header.SetLabel("Running")
		self._subheader.SetLabel('Please wait while the application performs its tasks. '
														'\nThis may take a few moments')
		self._settings_img.Hide() 
		self._running_img.Show()
		self.Layout()
	

	
	
	
	
	
	
	
	