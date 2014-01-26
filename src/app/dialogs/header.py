'''
Created on Dec 23, 2013

@author: Chris
'''

import wx
import imageutil
from app.dialogs.segoe_statictext import SegoeText

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
		self.header = self._bold_static_text(heading)
		self.subheader = wx.StaticText(self, label=subheading)
		self.img = self._load_image(image_path)
		
	def _do_layout(self):
		vsizer = wx.BoxSizer(wx.VERTICAL)
		sizer = wx.BoxSizer(wx.HORIZONTAL)
		headings_sizer = self.build_heading_sizer()
		sizer.Add(headings_sizer, 1, wx.ALIGN_LEFT | wx.EXPAND | wx.LEFT, PAD_SIZE)
		sizer.Add(self.img, 0, wx.ALIGN_RIGHT | wx.EXPAND | wx.RIGHT, PAD_SIZE)
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
		sizer.Add(self.header, 1)
		sizer.Add(self.subheader, 1)
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

	def UpdateImage(self, image):
		pass

	def RegisterController(self, controller):
		if self._controller is None: 
			self._controller = controller
	
	
	
	
	
	
	
	