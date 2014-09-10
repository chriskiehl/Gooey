'''
Created on Dec 11, 2013

@author: Chris

Collection of functions for extracting argparse related statements from the 
client code.
'''

import re
import os
import ast
import _ast
from itertools import *

import codegen
from gooey import modules


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
    *	argparse_assignments   	The assignment of the ArgumentParser (line 1 in example code)
    * add_arg_assignments     Calls to add_argument() (lines 2-3 in example code)
    * parser_var_name					The instance variable of the ArgumentParser (line 1 in example code)
    * ast_source							The curated collection of all parser related nodes in the client code
  """

  nodes = ast.parse(_openfile(file_name))

  module_imports = get_nodes_by_instance_type(nodes, _ast.Import)
  specific_imports = get_nodes_by_instance_type(nodes, _ast.ImportFrom)

  assignment_objs = get_nodes_by_instance_type(nodes, _ast.Assign)
  call_objects = get_nodes_by_instance_type(nodes, _ast.Call)

  argparse_assignments = get_nodes_by_containing_attr(assignment_objs, 'ArgumentParser')
  add_arg_assignments  = get_nodes_by_containing_attr(call_objects, 'add_argument')
  # parse_args_assignment = get_nodes_by_containing_attr(call_objects, 'parse_args')

  ast_argparse_source = chain(
    module_imports,
    specific_imports,
    argparse_assignments,
    add_arg_assignments
    # parse_args_assignment
  )
  # for i in ast_argparse_source:
  #   print i
  return ast_argparse_source

def _openfile(file_name):
  with open(file_name, 'rb') as f:
    return f.read()

def read_client_module(filename):
  with open(filename, 'r') as f:
    return f.readlines()

def get_nodes_by_instance_type(nodes, object_type):
  return [node for node in walk_tree(nodes) if isinstance(node, object_type)]

def get_nodes_by_containing_attr(nodes, attr):
  return [node for node in nodes if attr in walk_tree(node)]

def walk_tree(node):
  yield node
  d = node.__dict__
  for key, value in d.iteritems():
    if isinstance(value, list):
      for val in value:
        for _ in walk_tree(val): yield _
    elif 'ast' in str(type(value)):
      for _ in walk_tree(value): yield _
    else:
      yield value


def convert_to_python(ast_source):
  """
  Converts the ast objects back into human readable Python code
  """
  return map(codegen.to_source, ast_source)

def get_assignment_name(lines):
  nodes = ast.parse(''.join(lines))
  assignments = get_nodes_by_instance_type(nodes, _ast.Assign)
  argparse_var = get_nodes_by_containing_attr(assignments, 'parse_args')
  return argparse_var[0].value.func.value.id


def lines_indented(line):
  unindented = re.compile("^[a-zA-Z0-9_@]+")
  return unindented.match(line) is None

def not_at_main(line):
  return 'def main' not in line

def not_at_parse_args(line):
  return 'parse_args(' not in line

def get_indent(line):
  indent = re.compile("(\t|\s)")
  return ''.join(takewhile(lambda char: indent.match(char) is not None, line))

def format_source_to_return_parser(source):
  varname = get_assignment_name(source)

  client_source = [line for line in source
                   if '@gooey' not in line.lower()
                   and 'import gooey' not in line.lower()]

  top = takewhile(not_at_parse_args, client_source)
  middle = dropwhile(not_at_parse_args, client_source)
  # need this so the return statement is indented the
  # same amount as the rest of the source
  indent_width = get_indent(next(middle))

  # chew off everything until you get to the end of the
  # current block
  bottom = dropwhile(lines_indented, middle)
  # inject a return
  return_statement = ['{}return {}\n\n'.format(indent_width, varname)]
  # stitch it all back together
  new_source = chain(top, return_statement, bottom)
  return ''.join(new_source)

def extract_parser(modulepath):
  source = read_client_module(modulepath)
  module_source = format_source_to_return_parser(source)
  client_module = modules.load(module_source)
  return client_module.main()

if __name__ == '__main__':
  filepath = os.path.join(os.path.dirname(__file__),
                          'mockapplications',
                          'example_argparse_souce_in_main.py')

  nodes = ast.parse(_openfile(filepath))
  #
  ast_source = parse_source_file(filepath)
  python_code = convert_to_python(list(ast_source))
  for i in python_code: print i



