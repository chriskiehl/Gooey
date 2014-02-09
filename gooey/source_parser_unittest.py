'''
Created on Feb 2, 2014

@author: Chris
'''

import os
import ast
import unittest
import source_parser


class TestSourceParser(unittest.TestCase):
	PATH = os.path.join(os.path.dirname(__file__), 'mockapplications')
	
	def module_path(self, name):
		return os.path.join(self.PATH, name)
	
	def setUp(self):
		self._mockapp = self.module_path('mockapplications.py')
		self._module_with_noargparse = self.module_path('module_with_no_argparse.py')
		self._module_with_arparse_in_try = self.module_path('example_argparse_souce_in_try.py')
		self._module_with_argparse_in_main = self.module_path('example_argparse_souce_in_main.py')

	def test_parse_source_file__file_with_no_argparse__throws_parserexception(self):
		with self.assertRaises(source_parser.ParserError):
			source_parser.parse_source_file(self._module_with_noargparse)

	def test_parse_source_file__file_with_argparse_in_main__succesfully_finds_and_returns_ast_obejcts(self):
		ast_objects = source_parser.parse_source_file(self._module_with_argparse_in_main)
		for obj in ast_objects: 
			self.assertTrue(type(obj) in (ast.Assign, ast.Expr))
			
	def test_parse_source_file__file_with_argparse_in_try_block__succesfully_finds_and_returns_ast_obejcts(self):
		ast_objects = source_parser.parse_source_file(self._module_with_arparse_in_try)
		for obj in ast_objects: 
			self.assertTrue(type(obj) in (ast.Assign, ast.Expr))


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()