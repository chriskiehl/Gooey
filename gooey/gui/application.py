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
from gooey.gui.windows.advanced_config import AdvancedConfigPanel


def main():
  gooey_config = pull_cmd_args() if has_arg_supplied() else read_local_dir()

  if not os.path.exists(gooey_config):
    raise IOError('Gooey Config not found')

  with open(gooey_config, 'r') as f:
    build_spec = json.load(f)

  run(build_spec)


def run(build_spec):
  app = wx.App(False)

  i18n.load(build_spec['language'])

  BodyPanel = partial(AdvancedConfigPanel, build_spec=build_spec)

  frame = BaseWindow(BodyPanel, build_spec)

  frame.Show(True)
  app.MainLoop()


def pull_cmd_args():
  parser = argparse.ArgumentParser(description='Gooey turns your command line programs into beautiful, user friendly GUIs')
  parser.add_argument('file', help='Path to the configuration file for Gooey. We need this to run! :) ')
  args = parser.parse_args()
  return args.file

def read_local_dir():
  local_files = os.listdir(os.getcwd())
  if 'gooey_config.json' not in local_files:
    print "Bugger! gooey_config.json not found!"
    sys.exit(1)
  return os.path.join(os.getcwd(), 'gooey_config.json')

def has_arg_supplied():
  return len(sys.argv) > 1



if __name__ == '__main__':
  main()
