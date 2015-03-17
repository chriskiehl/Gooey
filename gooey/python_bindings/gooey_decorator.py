'''
Created on Jan 24, 2014

@author: Chris

Hey, whaduya know. This is out of date again. TODO: update giant doctring.


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

import wx
import os
import sys
import atexit
import tempfile
import source_parser

from gooey.gui import application
from gooey.gui.windows import layouts
from gooey.python_bindings import argparse_to_json


def Gooey(f=None, advanced=True,
          language='english', show_config=True,
          program_name=None, program_description=None):
  '''
  Decorator for client code's main function.
  Entry point for the GUI generator.

  Scans the client code for argparse data.
  If found, extracts it and build the proper
  configuration gui windows (basic or advanced).
  '''

  params = locals()

  def build(payload):
    def inner():
      show_config = params['show_config'] #because nonlocal keyword doesn't exist yet :(

      main_module_path = get_caller_path()
      _, filename = os.path.split(main_module_path)
      cleaned_source = clean_source(main_module_path)

      descriptor, tmp_filepath = tempfile.mkstemp(suffix='.py')
      atexit.register(cleanup, descriptor, tmp_filepath)

      with open(tmp_filepath, 'w') as f:
        f.write(cleaned_source)

      if not has_argparse(cleaned_source):
        show_config = False

      run_cmd = 'python {}'.format(tmp_filepath)

      # Must be called before anything else
      app = wx.App(False)

      build_spec = {
        'language': language,
        'target': run_cmd,
        'program_name': program_name or os.path.basename(sys.argv[0].replace('.py', '')),
        'program_description': program_description or '',
        'show_config': show_config,
        'show_advanced': advanced,
        'default_size': (610, 530),
        'requireds_cols': 1,
        'optionals_cols': 4,
        'manual_start': False
      }

      if show_config:
        parser = get_parser(main_module_path)
        build_spec['program_description'] = parser.description or program_description

        layout_data = argparse_to_json.convert(parser) if advanced else layouts.basic_config.items()
        build_spec.update(layout_data)

      else:
        build_spec['manual_start'] = True

      application.run(build_spec)

    inner.__name__ = payload.__name__
    return inner

  if callable(f):
    return build(f)
  return build


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

def has_argparse(source):
  bla = ['.parse_args(' in line.lower() for line in source.split('\n')]
  return any(bla)

def cleanup(descriptor, filepath):
  os.close(descriptor)
  os.remove(filepath)


if __name__ == '__main__':
  pass
