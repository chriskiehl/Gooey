from gooey.python_bindings import modules

__author__ = 'Chris'

import unittest


class TestModules(unittest.TestCase):

  def test_load_creates_and_imports_module_from_string_source(self):
    module_source = '''
some_var = 1234

def fooey():
  return 10

    '''
    module = modules.load(module_source)
    self.assertEqual(10, module.fooey())


  def test_generate_pyfilename_does_not_begin_with_digit(self):
    self.assertTrue(not modules.generate_pyfilename()[0].isdigit())
