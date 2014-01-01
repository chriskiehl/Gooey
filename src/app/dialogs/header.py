'''
Created on Dec 23, 2013

@author: Chris
'''

import wx

class FrameHeader(wx.Panel):
	
	def __init__(self,
				heading="Doin Stuff here",
				subheading="Small notification or intructional message",
				image_path=None,
				dlg_style=1,
				**kwargs):

		wx.Panel.__init__(self, **kwargs)
		self.SetBackgroundColour('#ffffff')
		self.SetMinSize((120, 90))

		header = self._bold_static_text(label=heading)
		subheader = wx.StaticText(self, label=subheading)
		img = self._load_image(image_path)
		
		sizer = wx.BoxSizer(wx.HORIZONTAL)
		headings_sizer = self.build_heading_sizer(header, subheader)
		sizer.Add(headings_sizer, 1, wx.ALIGN_LEFT | wx.EXPAND | wx.LEFT, 20)
		sizer.Add(img, 0, wx.ALIGN_RIGHT | wx.EXPAND | wx.RIGHT, 20)
		self.SetSizer(sizer)

		# for i in dir(self): print i 

	def _load_image(self, image_path):
		try:
				bitmap = wx.Bitmap(image_path)

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

	def _bold_static_text(self, label):
		txt = wx.StaticText(self, label=label)
		txt.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT,
				wx.FONTWEIGHT_NORMAL, wx.FONTWEIGHT_BOLD, False)
		)
		return txt 

	def build_heading_sizer(self, header, subheader):
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.AddStretchSpacer(1)
		sizer.Add(header, 1)
		sizer.Add(subheader, 1)
		sizer.AddStretchSpacer(1)
		return sizer