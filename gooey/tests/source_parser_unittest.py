# '''
# Created on Feb 2, 2014
#
# @author: Chris
#
# TODO:
#   - test no argparse module
#   - test argparse in main
#   - test argparse in try/catch
#   -
#
# '''
#
# import os
# import ast
# import unittest
# from gooey.python_bindings import source_parser
#
#
# basic_pyfile = \
# '''
# import os
#
# def say_jello():
#   print "Jello!"
#
# def main():
#   print "hello!"
#   parser = ArgumentParser(description='Example Argparse Program', formatter_class=RawDescriptionHelpFormatter)
#   parser.add_argument("filename", help="filename")
#   parser.add_argument("-r", "--recursive", dest="recurse", action="store_true",
#                       help="recurse into subfolders [default: %(default)s]")
#   parser.add_argument("-v", "--verbose", dest="verbose", action="count",
#                       help="set verbosity level [default: %(default)s]")
#   parser.add_argument("-i", "--include", action="append",
#                       help="only include paths matching this regex pattern. Note: exclude is given preference over include. [default: %(default)s]",
#                       metavar="RE")
#   parser.add_argument("-m", "--mycoolargument", help="mycoolargument")
#   parser.add_argument("-e", "--exclude", dest="exclude",
#                       help="exclude paths matching this regex pattern. [default: %(default)s]", metavar="RE")
#   parser.add_argument('-V', '--version', action='version')
#   parser.add_argument('-T', '--tester', choices=['yes', 'no'])
#   parser.add_argument(dest="paths", help="paths to folder(s) with source file(s) [default: %(default)s]",
#                       metavar="path", nargs='+')
#
# if __name__ == '__main__':
#   main()
# '''
#
#
#
# class TestSourceParser(unittest.TestCase):
#   PATH = os.path.join(os.path.dirname(__file__), 'examples')
#
#   def module_path(self, name):
#     return os.path.join(self.PATH, name)
#
#   def setUp(self):
#     self._mockapp = self.module_path('examples.py')
#     self._module_with_noargparse = self.module_path('module_with_no_argparse.py')
#     self._module_with_arparse_in_try = self.module_path('TODO.py')
#     self._module_with_argparse_in_main = self.module_path('example_argparse_souce_in_main.py')
#
#   def test_should_throw_parser_exception_if_no_argparse_found_in_module(self):
#     with self.assertRaises(source_parser.ParserError):
#       source_parser.parse_source_file(self._module_with_noargparse)
#
#
#   def test_find_main(self):
#     example_source = '''
# def main():  pass
#     '''
#     nodes = ast.parse(example_source)
#     main_node = source_parser.find_main(nodes)
#     self.assertEqual('main', main_node.name)
#
#
#   def test_find_main_throws_exception_if_not_found(self):
#     example_source = '''
# def some_cool_function_that_is_not_main():  pass
#     '''
#     with self.assertRaises(source_parser.ParserError):
#       nodes = ast.parse(example_source)
#       main_node = source_parser.find_main(nodes)
#       self.assertEqual('main', main_node.name)
#
#
#   def test_find_try_blocks_finds_all_tryblock_styles(self):
#     example_source = '''
# try: a = 1
# except: pass
#
# try: pass
# finally: pass
#
# try: pass
# except: pass
# else: pass
#     '''
#     nodes = ast.parse(example_source)
#     try_blocks = source_parser.find_try_blocks(nodes)
#     self.assertEqual(3, len(try_blocks))
#
#
#   def test_find_try_blocks_returns_empty_if_no_blocks_present(self):
#     example_source = 'def main(): pass'
#     nodes = ast.parse(example_source)
#     result = source_parser.find_try_blocks(nodes)
#     self.assertEqual(list(), result)
#
#   def test_find_argparse_located_object_when_imported_by_direct_name(self):
#     example_source = '''
# def main():
#   parser = ArgumentParser(description='Example Argparse Program', formatter_class=RawDescriptionHelpFormatter)
#     '''
#     nodes = ast.parse(example_source)
#     main_node = source_parser.find_main(nodes)
#     self.assertEqual('main', main_node.name)
#     containing_block = source_parser.find_block_containing_argparse([main_node])
#     self.assertTrue(containing_block is not None)
#
#   def test_find_argparse_located_object_when_access_through_module_dot_notation(self):
#     example_source = '''
# def main():
#   parser = argparse.ArgumentParser(description='Example Argparse Program', formatter_class=RawDescriptionHelpFormatter)
#     '''
#     nodes = ast.parse(example_source)
#     main_node = source_parser.find_main(nodes)
#     self.assertEqual('main', main_node.name)
#     containing_block = source_parser.find_block_containing_argparse([main_node])
#     self.assertTrue(containing_block is not None)
#
#   def test_find_argparse_locates_assignment_stmnt_in_main(self):
#     nodes = ast.parse(source_parser._openfile(self._module_with_argparse_in_main))
#     main_node = source_parser.find_main(nodes)
#     self.assertEqual('main', main_node.name)
#     containing_block = source_parser.find_block_containing_argparse([main_node])
#     self.assertTrue(containing_block is not None)
#     self.assertEqual('main', containing_block.name)
#
#
#   def test_find_argparse_locates_assignment_stmnt_in_try_block(self):
#     nodes = ast.parse(source_parser._openfile(self._module_with_arparse_in_try))
#     main_node = source_parser.find_main(nodes)
#     self.assertEqual('main', main_node.name)
#     try_nodes = source_parser.find_try_blocks(main_node)
#     self.assertTrue(len(try_nodes) > 0)
#     containing_block = source_parser.find_block_containing_argparse([main_node] + try_nodes)
#     self.assertEqual(ast.TryExcept, type(containing_block))
#
#
#   def test_find_argparse_throws_exception_if_not_found(self):
#     with self.assertRaises(source_parser.ParserError):
#       nodes = ast.parse(source_parser._openfile(self._module_with_noargparse))
#       main_node = source_parser.find_main(nodes)
#       self.assertEqual('main', main_node.name)
#       try_nodes = source_parser.find_try_blocks(main_node)
#       containing_block = source_parser.find_block_containing_argparse([main_node] + try_nodes)
#
#
#   def test_has_instantiator_returns_true_if_object_found(self):
#     source = '''
# parser = ArgumentParser(description='Example Argparse Program', formatter_class=RawDescriptionHelpFormatter)
# parser.add_argument("filename", help="filename")
#     '''
#     nodes = ast.parse(source)
#     self.assertTrue(source_parser.has_instantiator(nodes.body[0], 'ArgumentParser'))
#
#
#   def test_has_instantiator_returns_false_if_object_not_found(self):
#     source = '''
# parser = NopeParser(description='Example Argparse Program', formatter_class=RawDescriptionHelpFormatter)
# parser.add_argument("filename", help="filename")
#     '''
#     nodes = ast.parse(source)
#     self.assertFalse(source_parser.has_instantiator(nodes.body[0], 'ArgumentParser'))
#
#   def test_has_assignment_returns_true_if_object_found(self):
#     source = '''
# parser = ArgumentParser(description='Example Argparse Program', formatter_class=RawDescriptionHelpFormatter)
# parser.add_argument("filename", help="filename")
#     '''
#     nodes = ast.parse(source)
#     self.assertTrue(source_parser.has_assignment(nodes.body[1], 'add_argument'))
#
#   def test_has_assignment_returns_false_if_object_not_found(self):
#     source = '''
# parser = ArgumentParser(description='Example Argparse Program', formatter_class=RawDescriptionHelpFormatter)
# parser.add_argument("filename", help="filename")
#     '''
#     nodes = ast.parse(source)
#     self.assertFalse(source_parser.has_instantiator(nodes.body[1], 'add_argument'))
#
#   def test_parser_identifies_import_module(self):
#     source = '''
# import os
# import itertools
# from os import path
#     '''
#     import _ast
#     nodes = ast.parse(source)
#     module_imports = source_parser.get_nodes_by_instance_type(nodes, _ast.Import)
#     self.assertEqual(2, len(module_imports))
#
#   def test_parser_identifies_import_from(self):
#     source = '''
# import os
# import itertools
# from os import path
# from gooey.gooey_decorator import Gooey
#     '''
#     import _ast
#     nodes = ast.parse(source)
#     from_imports = source_parser.get_nodes_by_instance_type(nodes, _ast.ImportFrom)
#     self.assertEqual(2, len(from_imports))
#
#
#   def test_get_indent_return_indent_amount_for_tabs_and_spaces(self):
#     spaced_lines = ["def main"," def main","  def main","    def main"]
#     expected_indent = ["", " ", "  ", "    "]
#     for line, expected in zip(spaced_lines, expected_indent):
#       self.assertEqual(expected, source_parser.get_indent(line))
#
#   # def test_parse_source_file__file_with_argparse_in_main__succesfully_finds_and_returns_ast_obejcts(self):
#   #   ast_objects = source_parser.parse_source_file(self._module_with_argparse_in_main)
#   #   for obj in ast_objects:
#   #     self.assertTrue(type(obj) in (ast.Assign, ast.Expr))
#   #
#   # def test_parse_source_file__file_with_argparse_in_try_block__succesfully_finds_and_returns_ast_obejcts(self):
#   #   ast_objects = source_parser.parse_source_file(self._module_with_arparse_in_try)
#   #   for obj in ast_objects:
#   #     self.assertTrue(type(obj) in (ast.Assign, ast.Expr))
#
#
# if __name__ == "__main__":
#   #import sys;sys.argv = ['', 'Test.testName']
#   unittest.main()
#
