'''
Created on Dec 11, 2013

@author: Chris

Collection of functions for extracting argparse related statements from the 
client code. 



'''

import os 
import ast 
import codegen
from itertools import chain
from monkey_parser import MonkeyParser
from app.dialogs.action_sorter import ActionSorter
from parser_exceptions import ParserError




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
		raise ParserError("Could not locate AugmentParser.")
	
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
	raise ParserError('Could not find main function')


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
	'''
	Converts the ast objects back into Python code
	'''
	return map(codegen.to_source, ast_source)	


def extract_parser(modulepath):
	ast_source = parse_source_file(modulepath)
	if ast_source:
		python_code = convert_to_python(ast_source)
		return MonkeyParser(python_code)
	return None


if __name__ == '__main__':
	filepath = os.path.join(os.path.dirname(__file__), 
													'mockapplications', 
													'example_argparse_souce.py')
	ast_source = parse_source_file(filepath)
	python_code = convert_to_python(ast_source)
	parser = MonkeyParser(python_code)
	factory = ActionSorter(parser._actions)
	print factory._positionals
	
# 	
	

