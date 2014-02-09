'''
Created on Jan 24, 2014

@author: Chris
'''

import os
import wx 
import sys
import argparse 
import source_parser
from app.dialogs.config_model import ConfigModel, EmptyConfigModel

from app.dialogs import window
from app.dialogs.base_window import BaseWindow
from app.dialogs.advanced_config import AdvancedConfigPanel
from app.dialogs.basic_config_panel import BasicConfigPanel
from i18n import I18N
from functools import partial


def Gooey(f=None, advanced=True, 
				language='english', noconfig=False,
				program_name=None, program_description=None):
	'''
	Decorator for client code's main function. 
	Entry point for the GUI generator.  
	
	Scans the client code for argparse data. 
	If found, extracts it and build the proper 
	configuration page (basic or advanced). 
	'''
	
	params= locals()
	
	def build(f):
		def inner():
			module_path = get_caller_path()
			
			# Must be called before anything else
			app = wx.App(False)  
			
			if not noconfig:
				try:
					parser = source_parser.extract_parser(module_path)
				except source_parser.ParserError:
					raise source_parser.ParserError(
																	'Could not locate ArgumentParser statements.'
																	'\nPlease checkout github.com/chriskiehl/gooey to file a bug')
				model = ConfigModel(parser)
				if advanced:
					BodyPanel = partial(AdvancedConfigPanel, model=model) 
				else: 
					BodyPanel = BasicConfigPanel

			# User doesn't want to display configuration screen 
			# Just jump straight to the run panel
			else:
				BodyPanel = BasicConfigPanel
				model = EmptyConfigModel()
			
			frame = BaseWindow(BodyPanel, model, f, params)
			if noconfig:
				# gah, hacky.. not sure how else to go 
				# about it without rewriting a *bunch* of other stuff
				frame.ManualStart()
			frame.Show(True) 
			app.MainLoop() 

		inner.__name__ = f.__name__ 
		return inner

	if callable(f):
		return build(f)
	return build

def get_program_name(path):
	return '{}'.format(os.path.split(path)[-1])

def get_caller_path():
	# utility func for decorator
	# gets the name of the calling script
	tmp_sys = __import__('sys')
	return tmp_sys.argv[0]


if __name__ == '__main__':
	pass				