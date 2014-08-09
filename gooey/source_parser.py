'''
Created on Dec 11, 2013

@author: Chris

Collection of functions for extracting argparse related statements from the 
client code.
'''

import os
import ast
from itertools import chain

import codegen
from monkey_parser import MonkeyParser
from gooey.gui.action_sorter import ActionSorter
from parser_exceptions import ParserError


def parse_source_file(file_name):
  """
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
    * ast_source							The curated collection of all parser related nodes in the client code
  """

  nodes = ast.parse(_openfile(file_name))

  _mainfunc_block = find_main(nodes)
  _try_blocks = find_try_blocks(_mainfunc_block)

  nodes_to_search = chain([_mainfunc_block], _try_blocks)

  main_block = find_block_containing_argparse(nodes_to_search)

  argparse_assign_obj = find_assignment_objects(main_block)
  parser_nodes = find_parser_nodes(main_block)
  full_ast_source = chain(argparse_assign_obj, parser_nodes)
  return full_ast_source


def _openfile(file_name):
  with open(file_name, 'rb') as f:
    return f.read()


def find_main(nodes):
  code_block = _find_block(nodes, ast.FunctionDef, lambda node: node.name == 'main')
  if code_block != None:
    return code_block
  else:
    raise ParserError('Could not find main function')


def find_try_blocks(nodes):
  return _find_blocks(nodes, [ast.TryExcept, ast.TryFinally], lambda x: x)


def find_imports(nodes):
  return _find_blocks(nodes, ast.ImportFrom, lambda x: x.module == 'argparse')


def _find_block(nodes, types, predicate):
  blocks = _find_blocks(nodes, types, predicate)
  return blocks[0] if blocks else None


def _find_blocks(nodes, types, predicate):
  _types = types if isinstance(types, list) else [types]
  return [node
            for node in nodes.body
            if any([isinstance(node, _type) for _type in _types])
            and predicate(node)]


def find_block_containing_argparse(search_locations):
  # Browses a collection of Nodes for the one containing the Argparse instantiation
  for location in search_locations:
    if has_argparse_assignment(location):
      return location
  raise ParserError("Could not locate AugmentParser.")


def has_argparse_assignment(block):
  # Checks a given node for presence of an ArgumentParser instantiation
  argparse_assignment = _find_statement(block, has_instantiator, 'ArgumentParser')
  return is_found(argparse_assignment)


def find_assignment_objects(ast_block):
  return _find_statement(ast_block, has_instantiator, 'ArgumentParser')

def find_parser_nodes(ast_block):
  return _find_statement(ast_block, has_assignment, 'add_argument')


def is_found(stmnt):
  return len(stmnt)


def _find_statement(block, predicate, name):
  return [node for node in block.body
          if predicate(node, name)]


def has_instantiator(x, name):
  # Checks if the astObject is one with an instantiation of the ArgParse class
  return has_attr(name, lambda _name: x.value.func.id == _name)


def has_assignment(node, name):
  # Checks if the astObject contains a function with a name of name
  return has_attr(name, lambda _name: node.value.func.attr == _name)


def has_attr(name, attr_predicate):
  try:
    return attr_predicate(name)
  except AttributeError as e:
    return False  #  Wrong type. Ignore.


def get_assignment_name(node):
  # return the variable name to which ArgumentParser is assigned
  return node.targets[0].id


def convert_to_python(ast_source):
  """
  Converts the ast objects back into human readable Python code
  """
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
                          'example_argparse_souce_in_main.py')

  nodes = ast.parse(_openfile(filepath))

  ast_source = parse_source_file(filepath)
  python_code = convert_to_python(ast_source)
  parser = MonkeyParser(python_code)
  factory = ActionSorter(parser._actions)
  print factory._positionals



