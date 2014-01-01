'''
Created on Dec 12, 2013

@author: Chris
'''

# parser.add_argument("-r", "--recursive", dest="recurse", action="store_true", help="recurse into subfolders [default: %(default)s]")

class Option(object):
	def __init__(self, arg_option):
		self.arg_option = arg_option
		
	@classmethod
	def 