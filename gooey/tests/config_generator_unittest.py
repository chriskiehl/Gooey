import argparse
import pytest
from gooey.python_bindings.config_generator import *

# TODO: duplicated from argparse_to_json_unittest, should go into conftest.py
@pytest.fixture
def empty_parser():
  return argparse.ArgumentParser(description='description')


def test_create_from_parser(empty_parser):
  build_spec = create_from_parser(empty_parser,'.')
  assert build_spec['manual_start'] == True


def test_create_from_parser_show_config(empty_parser):
  build_spec = create_from_parser(empty_parser,
                                  '.',
                                  show_config=True)
  assert build_spec['program_description'] == 'description'
