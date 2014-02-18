'''
Created on Feb 8, 2014

@author: Chris
'''

import types
from argparse import ArgumentParser
from parser_exceptions import ArgumentError



class MonkeyParser(object):
	''' 
	Builds a parser instance from the code 
	extracted from the client module. 
	
	The instance is stored as a private variable in the 
	class and all methods are delagted to it so that the 
	user of the class can treat it just as a normal argparse 
	instance. 
	'''
	def __init__(self, source_code):
		self._parser_instance = self._build_argparser_from_client_source(source_code)
		# Monkey patch parser's `error` method so that it raises an error 
		# rather than silently exiting
		self._parser_instance.error = types.MethodType(
																							self._ErrorAsString, 
																							self._parser_instance)
		
	def _build_argparser_from_client_source(self, source_code):
		'''
		runs the client code by evaling each line. 
		
		Example input Code: 
		  parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
			parser.add_argument("-r", "--recursive", dest="recurse", action="store_true", help="recurse into subfolders [default: %(default)s]")
			parser.add_argument("-v", "--verbose", dest="verbose", action="count", help="set verbosity level [default: %(default)s]") 
			
		Method extracts the instance name (e.g. parser) from the first line, 
		and instantiates it in a local variable by evaling the rest of the lines.
		Each subsequent line updates the local variable in turn. 
		'''
		new_source_code = self._format_source_with_new_varname('clients_parser', source_code)
		# variable of the same name as the one passed into the format_source method. 
		# Used to hold the eval'd statements
		
		first_line = new_source_code.pop(0)
		clients_parser, assignment = self._split_line(first_line)
		
		clients_parser = eval(assignment)
		
		for line in new_source_code: 
			eval(line)
		return clients_parser
	
	def _format_source_with_new_varname(self, variable_name, source):
		'''
		'injects' the client code with a known variable name so that it 
		can be `eval`d and assigned to a variable in the local code. 
		
		For example, if the client code was:
			parser = ArgumentParser(descrip...)
			parser.add_argument("-r", "--re...)
			parser.add_argument("-v", "--ve...)
			
		The variable "parser" would be overwritten with a custom name. e.g. 
			my_parser = ArgumentParser(descrip...)
			my_parser.add_argument("-r", "--re...)
		'''
		source_code = source[:]
		
		first_line = source_code[0]
		parser_variable, statement = self._split_line(first_line)
		parser_variable = parser_variable.strip()
		
		for index, line in enumerate(source_code):
			source_code[index] = line.replace(parser_variable, variable_name)
		return source_code
		
	def _split_line(self, line):
		# Splits line at the first = sign, 
		# joins everything after the first = 
		# to account for additional = signs in 
		# parameters
		components = line.split('=')
		var = components.pop(0)
		return var, '='.join(components)
	
	def __getattr__(self, attr):
		''' 
		Auto-delegates everything to the ArgumentParser instance'''
		return getattr(self._parser_instance, attr)
	
	@staticmethod 
	def _ErrorAsString(self, msg):
		'''
		Monkey patch for parser.error
		Returns the error string rather than 
		printing and silently exiting. 
		'''
		raise ArgumentError(msg)
	
	
if __name__ == '__main__':
	pass
	
	
	