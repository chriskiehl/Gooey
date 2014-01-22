'''
Created on Jan 22, 2014

@author: Chris
'''

def Validate(parser, argument_string):
	try:
		parser.parse_args(argument_string.split())
	except:
		raise ValueError


if __name__ == '__main__':
	pass