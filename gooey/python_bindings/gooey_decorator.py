'''
Created on Jan 24, 2014

@author: Chris

TODO: this
'''

import json
import os
import sys
from argparse import ArgumentParser

from gooey.gui import application
from gooey.gui.util.freeze import get_resource_path
from . import config_generator

IGNORE_COMMAND = '--ignore-gooey'

def Gooey(f=None,
          advanced=True,
          language='english',
          auto_start=False,  # TODO: add this to the docs. Used to be `show_config=True`
          program_name=None,
          program_description=None,
          default_size=(610, 530),
          required_cols=2,
          optional_cols=2,
          dump_build_config=False,
          load_build_config=None,
          monospace_display=False, # TODO: add this to the docs
          image_dir='default',
          language_dir=get_resource_path('languages'),
          progress_regex=None, # TODO: add this to the docs
          progress_expr=None, # TODO: add this to the docs
          disable_progress_bar_animation=False,
          disable_stop_button=False,
          group_by_type=True): # TODO: add this to the docs
  '''
  Decorator for client code's main function.
  Serializes argparse data to JSON for use with the Gooey front end
  '''

  params = locals()

  def build(payload):
    def run_gooey(self, args=None, namespace=None):
      source_path = sys.argv[0]

      build_spec = None
      if load_build_config:
        try:
          build_spec = json.load(open(load_build_config, "r"))
        except Exception as e:
          print( 'Exception loading Build Config from {0}: {1}'.format(load_build_config, e))
          sys.exit(1)

      if not build_spec:
        build_spec = config_generator.create_from_parser(self, source_path, payload_name=payload.__name__, **params)

      if dump_build_config:
        config_path = os.path.join(os.getcwd(), 'gooey_config.json')
        print('Writing Build Config to: {}'.format(config_path))
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


if __name__ == '__main__':
  pass
