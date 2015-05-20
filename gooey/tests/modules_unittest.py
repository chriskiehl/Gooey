from gooey.python_bindings import modules

module_source = \
'''
some_var = 1234

def fooey():
  return 10

'''

def test_load_creates_and_imports_module_from_string_source():
    module = modules.load(module_source)
    assert 10 == module.fooey()


