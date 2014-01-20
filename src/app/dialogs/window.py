'''
Created on Jan 19, 2014

@author: Chris


def wrap():
	
	Check if there is a parser in the client code 
	
	if parser: 
		build WindowType based on parser
		showWindow()
		get user params
		pass params to sys.argv. 
		run client code
	
	else:
		Default WindowType
		run client code
		
		<wx._gdi.Bitmap; proxy of <Swig Object of type 'wxBitmap *' at 0x2ebf8e0> >
		<wx._gdi.Bitmap; proxy of <Swig Object of type 'wxBitmap *' at 0x2ebc830> >
'''

import wx 
import base_window
import advanced_config
from app.dialogs import argparse_test_data

def WithNoOptions(): pass 

def WithBasicOptions(): pass 

def WithAdvancedOptions(parser): 
	app = wx.App(False)  
	frame = base_window.BaseWindow(advanced_config.AdvancedConfigPanel, parser)
	frame.Show(True)     # Show the frame.
	app.MainLoop()

if __name__ == '__main__':
	parser = argparse_test_data.parser
	WithAdvancedOptions(parser)
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	