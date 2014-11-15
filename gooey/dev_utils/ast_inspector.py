from gooey.python_bindings import code_prep, source_parser

__author__ = 'Chris'

"""
Pretty Printing util for inspecting the various ast objects
"""

import ast
from _ast import Assign


def pretty_print(node, indent):
  d = node.__dict__
  for k, v in d.iteritems():
    if isinstance(v, list):
      print '-' * indent, k, ": "
      for i in v:
        pretty_print(i, indent + 2)
    elif 'ast' in str(type(v)):
      pretty_print(v, indent + 2)
    else:
      print '-' * indent, k, ": ", v


if __name__ == '__main__':
  lines = '''
def main():
  x = 1
  y = 2
  foo, doo = ("poo", "poo")
  smarser = argparse.ArgumentParser(description='Example Argparse Program', formatter_class=RawDescriptionHelpFormatter)
  random_junk = 123412353454356
  smarser.add_argument("filename", help="Name of the file you want to read")  # positional'
  smarser.add_argument("outfile", help="Name of the file where you'll save the output")  # positional
  bar = x + y
  baz = random_junk * 5
'''

  lines2 = '''
def main():
  try:
    foo, doo = ("poo", "poo")
    smarser = argparse.ArgumentParser(description='Example Argparse Program', formatter_class=RawDescriptionHelpFormatter)
    smarser.add_argument("filename", help="Name of the file you want to read")  # positional'
    smarser.add_argument("outfile", help="Name of the file where you'll save the output")  # positional
    smarser.parse_args()
  except:
    pass
'''

  git_example = '''

from argparse import ArgumentParser
def main():
    """Main"""
    bar = 'bar'
    print "Hello!"
    description='Desc'
    parser = ArgumentParser(description=bar)
    parser.add_argument(bar, help=('bar'))    ##################
    return parser
    # args = parser.parse_args()
    # print(args)
    # return True
  '''

  nodes = ast.parse(git_example)
  assign = source_parser.get_nodes_by_instance_type(nodes, Assign)
  assignment = source_parser.get_nodes_by_containing_attr(assign, "ArgumentParser")
  print assignment
  print assignment[0].__dict__
  p = source_parser.convert_to_python(assignment)[0]
  print p

  varname, instruction = code_prep.split_line(source_parser.convert_to_python(assignment)[0])

  updated_code = git_example.replace(varname, "jello_maker")

  print 'Fusdo:', updated_code.split('\n')[8]

  # all_code_leading_up_to_parseargs = '\n'.join(itertools.takewhile(lambda line: 'parse_args()' not in line, updated_code.split('\n')))
  # code = compile(all_code_leading_up_to_parseargs, '', 'exec')

  # exec(code)
  # parser = main()
  # print parser._actions



  # print assign[0].value.func.__dict__
  # print assign[0].value.keywords[0].value.__dict__
  # pretty_print(assign[0], 1)
