'''
Created on Jan 24, 2014

@author: Chris
'''

import os 
import sys
import argparse 
import source_parser
from app.dialogs import window


def Gooey(f=None, advanced=True, basic=False):
	'''
	Decorator for client code's main function. 
	Entry point for the GUI generator.  
	
	Scans the client code for argparse data. 
	If found, extracts it and build the proper 
	configuration page (basic or advanced). 
	
	Launched 
	
	'''

	# Handles if the passed in object is instance 
	# of ArgumentParser. If so, it's being called as 
	# a function, rather than a decorator
# 	if isinstance(f, argparse.ArgumentParser):
# 		progname = sys.argv[0]
# 
# 		build_doc_from_parser_obj(
# 			file_name=progname, 
# 			parser_obj=f, 
# 			format=format, 
# 			noob=noob, 
# 			success_msg=success_msg
# 			)
# 		return 

	# --------------------------------- #
	# Below code is all decorator stuff #
	# --------------------------------- #
	def build(f):
		def inner():
			module_path = get_caller_path()
			prog_name = get_program_name(module_path)
			parser = source_parser.pull_parser_from(module_path)
			window.WithAdvancedOptions(parser, f)
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