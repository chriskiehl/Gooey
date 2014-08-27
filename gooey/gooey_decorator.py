'''
Created on Jan 24, 2014

@author: Chris
'''

from functools import partial

import wx
from gooey.gui.component_factory import ComponentFactory

import i18n
import i18n_config
import source_parser
from gooey.gui.client_app import ClientApp
from gooey.gui.client_app import EmptyClientApp
from gooey.gui.base_window import BaseWindow
from gooey.gui.advanced_config import AdvancedConfigPanel
from gooey.gui.basic_config_panel import BasicConfigPanel


def Gooey(f=None, advanced=True,
          language='english', config=True,
          program_name=None, program_description=None):
  '''
  Decorator for client code's main function.
  Entry point for the GUI generator.

  Scans the client code for argparse data.
  If found, extracts it and build the proper
  configuration gui window (basic or advanced).
  '''

  params = locals()

  def build(payload):
    def inner():
      module_path = get_caller_path()

      # Must be called before anything else
      app = wx.App(False)

      i18n.load(language)

      if config:
        parser = get_parser(module_path)
        client_app = ClientApp(parser, payload)
        if advanced:
          BodyPanel = partial(AdvancedConfigPanel, action_groups=client_app.action_groups)
        else:
          BodyPanel = BasicConfigPanel
      # User doesn't want to display configuration screen
      # Just jump straight to the run panel
      else:
        BodyPanel = BasicConfigPanel
        client_app = EmptyClientApp()

      frame = BaseWindow(BodyPanel, client_app, params)

      if not config:
        frame.ManualStart()
      frame.Show(True)
      app.MainLoop()

    inner.__name__ = payload.__name__
    return inner

  if callable(f):
    return build(f)
  return build


def get_parser(module_path):
  try:
    return source_parser.extract_parser(module_path)
  except source_parser.ParserError:
    raise source_parser.ParserError(
      'Could not locate ArgumentParser statements in Main().'
      '\nThis is probably my fault :( Please checkout github.com/chriskiehl/gooey to file a bug!')

def get_caller_path():
  # utility func for decorator
  # gets the name of the calling script
  tmp_sys = __import__('sys')
  return tmp_sys.argv[0]


if __name__ == '__main__':
  pass