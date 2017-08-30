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

def Gooey(f=None,
          advanced=True,
          language='english',
          auto_start=False,  # TODO: add this to the docs. Used to be `show_config=True`
          target=None,
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
          group_by_type=True, # TODO: add this to the docs
          ignore_command='--ignore-gooey',
          force_command=None,
          load_cmd_args=False):
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
        cmd_args = None
        if load_cmd_args:
          try:
            cmd_args = self.original_parse_args()
          except:
            pass

        build_spec = config_generator.create_from_parser(self, source_path, cmd_args, payload_name=payload.__name__, **params)

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
    def inner2(*args, **kwargs):
      return func(*args, **kwargs)

    inner2.__name__ = func.__name__
    return inner2

  gooey = True
  if ignore_command and ignore_command in sys.argv:
    sys.argv.remove(ignore_command)
    gooey = False

  if force_command:
    if force_command in sys.argv:
      sys.argv.remove(force_command)
    else:
      gooey = False

  if gooey:
    if callable(f):
        return build(f)
    return build
  else:
    if callable(f):
      return run_without_gooey(f)
    return run_without_gooey


if __name__ == '__main__':
  pass
