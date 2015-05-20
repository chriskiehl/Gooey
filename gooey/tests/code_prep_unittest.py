__author__ = 'Chris'

import unittest
from gooey.python_bindings import code_prep


def test_split_line():
  line = "parser = ArgumentParser(description='Example Argparse Program')"
  assert "parser" == code_prep.split_line(line)[0]
  assert "ArgumentParser(description='Example Argparse Program')" == code_prep.split_line(line)[1]


def test_update_parser_varname_assigns_new_name_to_parser_var():
  line = ["parser = ArgumentParser(description='Example Argparse Program')"]
  expected = "jarser = ArgumentParser(description='Example Argparse Program')"
  result = code_prep.update_parser_varname('jarser', line)[0]
  assert result == expected

def test_update_parser_varname_assigns_new_name_to_parser_var__multiline():
  lines = '''
import argparse
from argparse import ArgumentParser
parser = ArgumentParser(description='Example Argparse Program')
parser.parse_args()
  '''.split('\n')

  line = "jarser = ArgumentParser(description='Example Argparse Program')"
  result = code_prep.update_parser_varname('jarser', lines)[2]
  assert line == result


def test_take_imports_drops_all_non_imports_statements():
  lines = '''
import argparse
from argparse import ArgumentParser
parser = ArgumentParser(description='Example Argparse Program')
parser.parse_args()
  '''.split('\n')[1:]

  assert 2 == len(list(code_prep.take_imports(lines)))
  assert 'import argparse' == list(code_prep.take_imports(lines))[0]


def test_drop_imports_excludes_all_imports_statements():
  lines = '''
import argparse
from argparse import ArgumentParser
parser = ArgumentParser(description='Example Argparse Program')
parser.parse_args()
  '''.split('\n')[1:]

  assert 2 == len(list(code_prep.take_imports(lines)))
  assert 'parser.parse_args()' == list(code_prep.drop_imports(lines))[1]


