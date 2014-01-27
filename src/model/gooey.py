'''
Created on Jan 24, 2014

@author: Chris
'''

import os 
import sys
import argparse 
import source_parser
from app.dialogs.config_model import Model
from app.dialogs import window
from model.i18n import I18N


def Gooey(f=None, advanced=True, language='english'):
	'''
	Decorator for client code's main function. 
	Entry point for the GUI generator.  
	
	Scans the client code for argparse data. 
	If found, extracts it and build the proper 
	configuration page (basic or advanced). 
	
	Launched 
	
	'''
	def build(f):
		def inner():
			module_path = get_caller_path()
			parser = source_parser.extract_parser(module_path)
			i18n = I18N(language)
			if not parser: 
				print 'shit fuck!'
				# run basic program with info window
				return 
# 			config_model = Model(parser)
# 			arg_string = 'asdf 5 -s'
# 			if not config_model.IsValidArgString(arg_string):
# 				error = config_model.GetErrorMsg(arg_string)
# 				raise ValueError("you suck, son! \n%s" % error)
# 			config_model.AddToArgv(arg_string)
# 			f()
# 			
# 			if advanced:
			window.WithAdvancedOptions(parser, f)
# 			else:
# 				pass # run simple congig version
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