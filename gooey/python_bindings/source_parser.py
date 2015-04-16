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

from gooey.python_bindings import codegen, modules


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
  parse_args_assignment = get_nodes_by_containing_attr(call_objects, 'parse_args')

  ast_argparse_source = chain(
    module_imports,
    specific_imports,
    argparse_assignments,
    add_arg_assignments
    # parse_args_assignment
  )
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

def format_source_to_return_parser(source, cutoff_line, restart_line, col_offset, parser_name):
  top = source[:cutoff_line - 1]
  bottom = source[restart_line:]
  indentation = source[cutoff_line - 1][:col_offset]
  return_statement = ['{}return {}\n\n'.format(indentation, parser_name)]

  # stitch it all back together excluding the Gooey decorator
  new_source = (line for line in chain(top, return_statement, bottom)
                if '@gooey' not in line.lower())

  return ''.join(new_source)

def extract_parser(modulepath, func_with_argparse):
  source = read_client_module(modulepath)

  nodes = ast.parse(''.join(source))
  funcs = get_nodes_by_instance_type(nodes, _ast.FunctionDef)
  assignment_objs = get_nodes_by_instance_type(nodes, _ast.Assign)

  main_func = get_nodes_by_containing_attr(funcs, func_with_argparse)[0]
  parse_args_assignment = get_nodes_by_containing_attr(main_func.body, 'parse_args')[0]

  # ast reports the line no of a block structure as the start of the structure,
  # not the end, so we look for the line no of the next node after main()
  # and use that as the end of the main() function.
  try:
    restart_line = nodes.body[nodes.body.index(main_func)+1].lineno - 1
  except IndexError:
    restart_line = len(source)

  module_source = format_source_to_return_parser(
    source,
    cutoff_line=parse_args_assignment.lineno,
    restart_line=restart_line,
    col_offset=parse_args_assignment.col_offset,
    parser_name=parse_args_assignment.value.func.value.id
  )
  client_module = modules.load(module_source)
  return getattr(client_module, func_with_argparse)()


def has_argparse(source):
  return any(['.parse_args(' in line.lower() for line in source.split('\n')])

if __name__ == '__main__':
  filepath = os.path.join(os.path.dirname(__file__),
                          'examples',
                          'example_argparse_souce_in_main.py')

  nodes = ast.parse(_openfile(filepath))
  #
  ast_source = parse_source_file(filepath)
  python_code = convert_to_python(list(ast_source))



