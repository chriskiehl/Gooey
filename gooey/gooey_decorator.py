'''
Created on Jan 24, 2014

@author: Chris

##How things work these days (though, likely to change)

The decorator is used solely as a nice way to get the location
of the executing script. It no longer returns a decorated version
of the client code, but in fact completely hijacks the execution.
So, rather than returning a reference to the client's main, it now
returns itself, thus short-circuiting the execution of the client
program.

What it DOES do now is grab where the client module is stored and
read it in as a file so that it can hack away at it.

The first step, as before, is getting the ArgumentParser reference
so that the needed values can be extracted. This is done by reading
the source file up to the point where the `parse_args()` method is
called. This puts us smack in the middle of the client's `main` method.

This first half guarantees that all imports, modules, variable assignments,
etc.. are caught (unlike before).

Next step: getting the rest of the source code that's relevant

The file is again read up to the `parse_args` call, but this time everything
leading up to that point is dropped and we keep only the remainder of the file.
So, now the top and the bottom is located, but the bottom needs to be trimmed a
little more -- we want to drop everything remaining in the main method.

So, we `dropwhile` lines are currently indented (and thus still part of the `main`
method)

Finally, we arrive at the end, which gives us an exact copy of the original source
file, minus all of it's main logic. The two pieces are then sandwiched together,
saved to a file, and imported as a new module. Now all that has to be done is call
it (moddified) main function, and bam! It returns to fully populated parser object
to us. No more complicated ast stuff. Just a little bit of string parsing and we're
done.

'''

from functools import partial

import wx
from gooey.gui.component_factory import ComponentFactory

import i18n
import i18n_config
import source_parser

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

      # load gui components after loading the language pack
      from gooey.gui.client_app import ClientApp
      from gooey.gui.client_app import EmptyClientApp
      from gooey.gui.base_window import BaseWindow
      from gooey.gui.advanced_config import AdvancedConfigPanel
      from gooey.gui.basic_config_panel import BasicConfigPanel

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
        client_app = EmptyClientApp(payload)

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
  # try:
  return source_parser.extract_parser(module_path)
  # except source_parser.ParserError:
  #   raise source_parser.ParserError(
  #     'Could not locate ArgumentParser statements in Main().'
  #     '\nThis is probably my fault :( Please checkout github.com/chriskiehl/gooey to file a bug!')

def get_caller_path():
  # utility func for decorator
  # gets the name of the calling script
  tmp_sys = __import__('sys')
  return tmp_sys.argv[0]


if __name__ == '__main__':
  pass
