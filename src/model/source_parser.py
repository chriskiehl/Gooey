'''
Created on Dec 11, 2013

@author: Chris

Collection of functions for extracting argparse related statements from the 
client code. 



'''

import os 
import ast 
import sys
import random
import codegen
import argparse
import cStringIO
from itertools import chain
from functools import partial 
from numpy.lib.utils import _split_line
from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
from app.dialogs.action_sorter import ActionSorter


class ParserError(Exception):
	'''Thrown when the parser can't find argparse functions the client code'''
	pass


class ParserFromSource(object):
	''' 
	Builds a parser instance from the code 
	extracted from the client module. 
	
	The instance is stored as a private variabel in the 
	class and all methods are delagted to it so that the 
	user of the class can treat it just as a normal argparse 
	instance. 
	'''
	def __init__(self, source_code):
		self._parser_instance = self._build_argparser_from_client_source(source_code)
		# redirect future getattr requests
# 		self.__getattr__ = self._delegator
		
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
	

def parse_source_file(file_name):
	'''
	Parses the AST of Python file for lines containing 
	references to the argparse module. 
	
	returns the collection of ast objects found.
	
	Example client code:
	 
		1. parser = ArgumentParser(desc="My help Message")
		2. parser.add_argument('filename', help="Name of the file to load")
		3. parser.add_argument('-f', '--format', help='Format of output \nOptions: ['md', 'html']
		4. args = parser.parse_args() 
	
	Variables:
		* nodes 									Primary syntax tree object
		* _mainfunc_block					main() method as found in the ast nodes
		* _try_blocks							Try/except/finally blocks found in the main method
		* main_block 							The code block in which the ArgumentParser statements are located 
		*	argparse_assign_obj   	The assignment of the ArgumentParser (line 1 in example code)
		* parser_nodes						Nodes which have parser references (lines 1-4 in example code)
		* parser_var_name					The instance variable of the ArgumentParser (line 1 in example code)
		* ast_source							The currated colleciton of all parser related nodes in the client code
	'''
	
	nodes = ast.parse(_openfile(file_name))
	
	_mainfunc_block = find_main(nodes)
	_try_blocks = find_try_blocks(_mainfunc_block)
	
	search_locations = chain([_mainfunc_block], _try_blocks)
	
	main_block = find_argparse_location(search_locations)
	if not main_block: 
		raise ParserError("Could not locate AugmentParser assignment.")
	
	argparse_assign_obj = [node for node in main_block.body
									if has_instantiator(node, 'ArgumentParser')]
	
	parser_nodes = [node for node in main_block.body
									if has_assignment(node, 'add_argument')]
	
	ast_source = chain(argparse_assign_obj, parser_nodes)
	return ast_source


def find_try_blocks(block):
	# Finds all try/catch/finally expressions in a given function block
	_types = [ast.TryExcept, ast.TryFinally]
	return [node for node in block.body 
					if any([isinstance(node, x) for x in _types])]
	
						
def find_main(nodes):
	# Finds main function in the tree 
	for node in nodes.body: 
		if isinstance(node, ast.FunctionDef) and node.name == 'main':
			return node
	raise ParserError('Could not find `def main()`')


def get_assignment_name(node): 
	# return the variable name to which 
	# ArgumentParser is assigned
	return node.targets[0].id 


def _openfile(file_name):
	with open(file_name, 'rb') as f: 
		return f.read()
	
	
def find_statement(block, name):
	return [node for node in block.body 
					if has_instantiator(node, name)]

def has_instantiator(x, name):
	# Checks if the astObject is one with an 
	# instantiation of the ArgParse class
	try: return x.value.func.id == name	
	except: return False #  Wrong type. Contine.

def has_assignment(x, name):
	# Checks if the astObject is contains a 
	# function with a name of name
	try: return x.value.func.attr == name	
	except: return False #  Wrong type. Contine.
	
def is_found(stmnt):
	return len(stmnt)

def has_argparse_assignment(block):
	# Checks a given node for presence of an instantiation
	argparse_assignment = find_statement(block, 'ArgumentParser')
	return is_found(argparse_assignment) 

def find_argparse_location(locations):
	# Browser a collection of Nodes for the one 
	# containing the Argparse instantiation
	for location in locations:
		if has_argparse_assignment(location):
			return location
	return None

def convert_to_python(ast_source):
	return map(codegen.to_source, ast_source)	

def generate_doc(f=None, format='html', noob=1, success_msg=1):
	'''
	Decorator for client code's main function. 
	It gets the name of the calling script, loads it 
	into parse_pyfile(), and generates the documentation, 
	before finally calling the main() function to resume 
	execution as normal. 
	'''

	# Handles if the passed in object is instance 
	# of ArgumentParser. If so, it's being called as 
	# a function, rather than a decorator
	if isinstance(f, argparse.ArgumentParser):
		filename = sys.argv[0]

		build_doc_from_parser_obj(
			file_name=filename, 
			parser_obj=f, 
			format=format, 
			noob=noob, 
			success_msg=success_msg
			)
		return 

	# --------------------------------- #
	# Below code is all decorator stuff #
	# --------------------------------- #
	def get_caller_path():
		# utility func for decorator
		# gets the name of the calling script
		tmp_sys = __import__('sys')
		return tmp_sys.argv[0]

	def generate_docs(f):
		def inner():
			module_path = get_caller_path()
			path = os.path.join(*os.path.split(module_path)[:-1])
			filename = '{}'.format(os.path.split(module_path)[-1])
			parse_pyfile(filename, format=format, noob=noob, success_msg=success_msg)
		inner.__name__ = f.__name__ 
		return inner

	if callable(f):
		return generate_docs(f)
	return generate_docs



if __name__ == '__main__':
	ast_source = parse_source_file('example_argparse_souce.py')
	python_code = convert_to_python(ast_source)
	parser = ParserFromSource(python_code)
	factory = ActionSorter(parser)
	print factory._positionals
	
# 	
	

