'''
Main runner entry point for Gooey.
'''

import wx
import os
import sys
import json
import argparse

from functools import partial

from gooey.gui.lang import i18n
from gooey.gui.windows.base_window import BaseWindow
from gooey.gui.windows.advanced_config import ConfigPanel

from gooey.python_bindings import config_generator, source_parser


def main():
  parser = argparse.ArgumentParser(
    description='Gooey turns your command line programs into beautiful, user friendly GUIs')

  parser.add_argument(
    '-b', '--create-build-script',
    dest='build_script',
    help='Parse the supplied Python File and generate a runnable Gooey build script'
  )

  parser.add_argument(
    '-r', '--run',
    dest='run',
    nargs='?',
    const='',
    help='Run Gooey with build_config in local dir OR via the supplied config path'
  )

  args = parser.parse_args()

  if args.build_script:
    do_build_script(args.build_script)
  elif args.run is not None:
    do_run(args)


def do_build_script(module_path):
  with open(module_path, 'r') as f:
    if not source_parser.has_argparse(f.read()):
      raise AssertionError('Argparse not found in module. Unable to continue')

  gooey_config = config_generator.create_from_parser(module_path, show_config=True)
  outfile = os.path.join(os.getcwd(), 'gooey_config.json')

  print 'Writing config file to: {}'.format(outfile)

  with open(outfile, 'w') as f:
    f.write(json.dumps(gooey_config, indent=2))


def do_run(args):
  gooey_config = args.run or read_local_dir()

  if not os.path.exists(gooey_config):
    raise IOError('Gooey Config not found')

  with open(gooey_config, 'r') as f:
    build_spec = json.load(f)
  run(build_spec)


def run(build_spec):
  app = wx.App(False)

  i18n.load(build_spec['language'])

  frame = BaseWindow(build_spec)
  frame.Show(True)
  app.MainLoop()


def read_local_dir():
  local_files = os.listdir(os.getcwd())
  if 'gooey_config.json' not in local_files:
    print "Bugger! gooey_config.json not found!"
    sys.exit(1)
  return os.path.join(os.getcwd(), 'gooey_config.json')


if __name__ == '__main__':
  main()
