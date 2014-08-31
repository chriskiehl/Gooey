from gooey import source_parser

__author__ = 'Chris'

"""
Pretty Printing util for inspecting the various ast objects
"""

import ast
from _ast import Assign, Call

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
  nodes = ast.parse(open(r'C:\Users\Chris\Dropbox\pretty_gui\Gooey\gooey\mockapplications\mockapp_import_argparse.py').read())

  pretty_print(nodes, 1)
