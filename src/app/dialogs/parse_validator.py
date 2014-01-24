'''
Created on Jan 22, 2014

@author: Chris
'''

import types 
from argparse import ArgumentParser








def validate(parser, arg_string):
	parser.error = types.MethodType(RaiseError, parser)
	parser.parse_args(arg_string.split())



if __name__ == '__main__':
	pass