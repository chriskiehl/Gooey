__author__ = 'Chris'

"""
Preps the extracted Python code so that it can be evaled by the
monkey_parser
"""

from itertools import *

source = '''
import sys
import os
import doctest
import cProfile
import pstats
from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
from gooey import Gooey
parser = ArgumentParser(description='Example Argparse Program', formatter_class=RawDescriptionHelpFormatter)
parser.add_argument('filename', help='filename')
parser.add_argument('-r', '--recursive', dest='recurse', action='store_true', help='recurse into subfolders [default: %(default)s]')
parser.add_argument('-v', '--verbose', dest='verbose', action='count', help='set verbosity level [default: %(default)s]')
parser.add_argument('-i', '--include', action='append', help='only include paths matching this regex pattern. Note: exclude is given preference over include. [default: %(default)s]', metavar='RE')
parser.add_argument('-m', '--mycoolargument', help='mycoolargument')
parser.add_argument('-e', '--exclude', dest='exclude', help='exclude paths matching this regex pattern. [default: %(default)s]', metavar='RE')
parser.add_argument('-V', '--version', action='version')
parser.add_argument('-T', '--tester', choices=['yes', 'no'])
parser.add_argument(dest='paths', help='paths to folder(s) with source file(s) [default: %(default)s]', metavar='path', nargs='+')
'''

def take_imports(code):
  return takewhile(lambda line: 'import' in line, code)

def drop_imports(code):
  return dropwhile(lambda line: 'import' in line, code)

def split_line(line):
  # splits an assignment statement into varname and command strings
  # in: "parser = ArgumentParser(description='Example Argparse Program')"
  # out: "parser", "ArgumentParser(description='Example Argparse Program"
  variable, instruction = line.split('=', 1)
  return variable.strip(), instruction.strip()

def update_parser_varname(new_varname, code):
  # lines = source.split('\n')[1:]
  lines = filter(lambda x: x != '', code)

  argparse_code = dropwhile(lambda line: 'import' in line, lines)
  old_argparser_varname, _ = split_line(argparse_code.next())

  updated_code = [line.replace(old_argparser_varname, new_varname)
                  for line in lines]
  return updated_code

if __name__ == '__main__':
  pass





