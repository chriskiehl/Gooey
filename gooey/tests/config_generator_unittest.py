from gooey.python_bindings.config_generator import *


def test_create_from_parser(empty_parser):
  build_spec = create_from_parser(empty_parser,'.')
  assert build_spec['manual_start'] == True


def test_create_from_parser_show_config(empty_parser):
  build_spec = create_from_parser(empty_parser,
                                  '.',
                                  show_config=True)
  assert build_spec['program_description'] == 'description'
