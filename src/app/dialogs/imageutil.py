'''
Created on Jan 20, 2014

@author: Chris
'''
import wx
from PIL import Image  # @UnresolvedImport
from app.images import image_store



def LoadAndResizeImage(path):
	im = Image.open(path)
	return PilImageToWxImage(_Resize(im))
	
def _Resize(pil_image):
	'''
	Resizes a bitmap to a height of 79 pixels (the 
	size of the top panel -1), while keeping aspect ratio 
	in tact
	'''
	target_size = _GetTargetSize(pil_image.size)
	return pil_image.resize(target_size)
	
def _GetTargetSize(size):
	width, height = size
	aspect_ratio = float(width)/height
	tHeight = 79
	tWidth = int(tHeight * aspect_ratio)
	return (tWidth, tHeight)	

def PilImageToWxImage(p_image):
	wx_image = wx.EmptyImage(*p_image.size)
	wx_image.SetData(p_image.convert( 'RGB' ).tostring())
	return wx_image.ConvertToBitmap()

if __name__ == '__main__':
	app = wx.App()
	print 'adsfasdf',LoadAndResizeImage(image_store.computer)
	print 'asdfadf'
	app.MainLoop()
	
	
	
	
	
	
	
	