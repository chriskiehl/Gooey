'''
Created on Jan 23, 2014

@author: Chris
'''

import sys
import types
from app.dialogs.action_sorter import ActionSorter

class ArgumentError(Exception):
	pass

class Model(object):
	_instance = None
	
	def __init__(self, parser=None):
		self._parser = parser 
		self.description = parser.description
		
		self.action_groups = ActionSorter(self._parser._actions) 
		
		# monkey patch
		print self._parser.error
		self._parser.error = types.MethodType(
																	self.ErrorAsString, 
																	self._parser)
		print self._parser.error
		
		Model._instance = self
	
	def HasPositionals(self):
		if self.action_groups._positionals:
			return True
		return False
	
	def IsValidArgString(self, arg_string):
		if isinstance(self._Parse(arg_string), str):
			return False
		return True
	
	def _Parse(self, arg_string):
		try: 
			print self._parser.error
			self._parser.parse_args(arg_string.split())
			return True
		except ArgumentError as e:
			return str(e)
		
	def GetErrorMsg(self, arg_string):
		return self._FormatMsg(self._Parse(arg_string))
		
	def _FormatMsg(self, msg):
		output = list(msg)
		if ':' in output:
			output[output.index(':')] = ':\n '
		return ''.join(output)
	
	def AddToArgv(self, arg_string):
		sys.argv.append(arg_string.split())
	
	@staticmethod 
	def ErrorAsString(self, msg):
		'''
		Monkey patch for parser.error
		Returns the error string rather than 
		printing and silently exiting. 
		'''
		raise ArgumentError(msg)
	
	@classmethod
	def GetInstance(cls):	
		return cls._instance



if __name__ == '__main__':
	pass
	
	
# 	print m2

	
	
	
