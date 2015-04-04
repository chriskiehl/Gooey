import itertools
import wx
import os
import sys
import json
import argparse

from functools import partial

from gooey.gui.lang import i18n
from gooey.gui.windows.base_window import BaseWindow
from gooey.gui.windows.advanced_config import AdvancedConfigPanel


def run(build_spec=None):
  if not build_spec:
    if len(sys.argv) > 1:
      parser = argparse.ArgumentParser(description='Gooey turns your command line programs into beautiful, user friendly GUIs')
      parser.add_argument('file', help='Path to the configuration file for Gooey. We need this to run! :) ')
      args = parser.parse_args()
      gooey_config = args.file
    else:
      local_files = os.listdir(os.getcwd())
      if 'gooey_config.json' not in local_files:
        print "Bugger! gooey_config.json not found!"
        sys.exit(1)
      gooey_config = os.path.join(os.getcwd(), 'gooey_config.json')

    if not os.path.exists(gooey_config):
      raise IOError('Gooey Config not found')

    with open(gooey_config, 'r') as f:
      build_spec = json.load(f)

  app = wx.App(False)

  i18n.load(build_spec['language'])

  BodyPanel = partial(AdvancedConfigPanel, build_spec=build_spec)

  frame = BaseWindow(BodyPanel, build_spec)

  frame.Show(True)
  app.MainLoop()








if __name__ == '__main__':
  run()
