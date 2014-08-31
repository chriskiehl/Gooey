__author__ = 'Chris'

import unittest
import code_prep

class TestCodePrep(unittest.TestCase):

  def test_split_line(self):
    line = "parser = ArgumentParser(description='Example Argparse Program')"
    self.assertEqual("parser", code_prep.split_line(line)[0])
    self.assertEqual("ArgumentParser(description='Example Argparse Program')", code_prep.split_line(line)[1])

  def test_update_parser_varname_assigns_new_name_to_parser_var(self):
    line = ["parser = ArgumentParser(description='Example Argparse Program')"]
    self.assertEqual(
      "jarser = ArgumentParser(description='Example Argparse Program')",
      code_prep.update_parser_varname('jarser', line)[0]
    )

  def test_update_parser_varname_assigns_new_name_to_parser_var__multiline(self):
    lines = '''
import argparse
from argparse import ArgumentParser
parser = ArgumentParser(description='Example Argparse Program')
parser.parse_args()
    '''.split('\n')

    self.assertEqual(
      "jarser = ArgumentParser(description='Example Argparse Program')",
      code_prep.update_parser_varname('jarser', lines)[2]
    )

  def test_take_imports_drops_all_non_imports_statements(self):
    lines = '''
import argparse
from argparse import ArgumentParser
parser = ArgumentParser(description='Example Argparse Program')
parser.parse_args()
    '''.split('\n')[1:]

    self.assertEqual(2, len(list(code_prep.take_imports(lines))))
    self.assertEqual('import argparse', list(code_prep.take_imports(lines))[0])

  def test_drop_imports_excludes_all_imports_statements(self):
    lines = '''
import argparse
from argparse import ArgumentParser
parser = ArgumentParser(description='Example Argparse Program')
parser.parse_args()
    '''.split('\n')[1:]

    self.assertEqual(2, len(list(code_prep.take_imports(lines))))
    self.assertEqual('parser.parse_args()', list(code_prep.drop_imports(lines))[1])

if __name__ == "__main__":
  #import sys;sys.argv = ['', 'Test.testName']
  unittest.main()
