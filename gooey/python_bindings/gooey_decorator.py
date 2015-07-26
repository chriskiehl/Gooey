'''
Created on Jan 24, 2014

@author: Chris

TODO: this
'''

import os
import json
import atexit
import tempfile

from . import source_parser
from . import config_generator
import sys

from gooey.gui import application

from argparse import ArgumentParser


IGNORE_COMMAND = '--ignore-gooey'

def Gooey(f=None,
          advanced=True,
          language='english',
          show_config=True,
          program_name=None,
          program_description=None,
          default_size=(610, 530),
          required_cols=2,
          optional_cols=2,
          dump_build_config=False,
          monospace_display=False):
  '''
  Decorator for client code's main function.
  Serializes argparse data to JSON for use with the Gooey front end
  '''

  params = locals()

  def build(payload):
    def run_gooey(self, args=None, namespace=None):
      source_path = sys.argv[0]
      build_spec = config_generator.create_from_parser(self, source_path, payload_name=payload.__name__, **params)

      if dump_build_config:
        config_path = os.path.join(os.getcwd(), 'gooey_config.json')
        print( 'Writing Build Config to: {}'.format(config_path))
        with open(config_path, 'w') as f:
          f.write(json.dumps(build_spec, indent=2))
      application.run(build_spec)

    def inner2(*args, **kwargs):
      ArgumentParser.original_parse_args = ArgumentParser.parse_args
      ArgumentParser.parse_args = run_gooey
      return payload(*args, **kwargs)

    inner2.__name__ = payload.__name__
    return inner2

  def run_without_gooey(func):
    return lambda: func()

  if IGNORE_COMMAND in sys.argv:
    sys.argv.remove(IGNORE_COMMAND)
    if callable(f):
      return run_without_gooey(f)
    return run_without_gooey

  if callable(f):
    return build(f)
  return build


def store_executable_copy():
  main_module_path = get_caller_path()
  _, filename = os.path.split(main_module_path)
  cleaned_source = clean_source(main_module_path)

  descriptor, tmp_filepath = tempfile.mkstemp(suffix='.py')
  atexit.register(cleanup, descriptor, tmp_filepath)

  with open(tmp_filepath, 'w') as f:
    f.write(cleaned_source)
  return tmp_filepath


def clean_source(module_path):
  with open(module_path, 'r') as f:
    return ''.join(
      line for line in f.readlines()
      if '@gooey' not in line.lower())


def get_parser(module_path):
  return source_parser.extract_parser(module_path)


def get_caller_path():
  tmp_sys = __import__('sys')
  return tmp_sys.argv[0]


def cleanup(descriptor, filepath):
  os.close(descriptor)
  os.remove(filepath)


if __name__ == '__main__':
  pass
