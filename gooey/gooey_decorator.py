'''
Created on Jan 24, 2014

@author: Chris
'''

from functools import partial

import wx

import i18n_config
import source_parser
from gooey.gui.config_model import ConfigModel
from gooey.gui.config_model import EmptyConfigModel
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

  def build(f):
    def inner():
      module_path = get_caller_path()

      # Must be called before anything else
      app = wx.App(False)

      load_language_pack(language)

      if config:
        parser = get_parser(module_path)
        model = ConfigModel(parser)
        if advanced:
          BodyPanel = partial(AdvancedConfigPanel, model=model)
        else:
          BodyPanel = BasicConfigPanel

      # User doesn't want to display configuration screen
      # Just jump straight to the run panel
      else:
        BodyPanel = BasicConfigPanel
        model = EmptyConfigModel()

      frame = BaseWindow(BodyPanel, model, f, params)
      if not config:
        # gah, hacky.. not sure how else to go
        # about it without rewriting a *bunch* of other stuff
        frame.ManualStart()
      frame.Show(True)
      app.MainLoop()

    inner.__name__ = f.__name__
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

def load_language_pack(language):
  if language is not 'english':
    i18n_config.LANG = language
  import i18n




if __name__ == '__main__':
  pass