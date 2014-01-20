'''
Created on Jan 20, 2014

@author: Chris
'''

import wx

class SegoeText(wx.StaticText):
	'''
	Convenience subclass of wx.StaticText. 
	
	Sets the default font to Segoe UI and 
	has methods fow easily changing size and weight
	'''


	def __init__(self, parent, label):
		wx.StaticText.__init__(self, parent, label=label)
		self._font = wx.Font(20, wx.FONTFAMILY_DEFAULT,
				wx.FONTWEIGHT_NORMAL, wx.FONTWEIGHT_BOLD, False,
				'Segoe UI Light')
		
		self.SetFont(self._font)
		
	def SetWeight(self, weight):
		pass
				