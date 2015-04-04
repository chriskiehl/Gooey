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
import json

import os
import sys
import atexit
import tempfile
import source_parser
import config_generator

from gooey.gui import application
from gooey.gui.windows import layouts
from gooey.python_bindings import argparse_to_json


def Gooey(f=None,
          advanced=True,
          language='english',
          show_config=True,
          program_name=None,
          program_description=None,
          dump_build_config=False):
  '''
  Decorator for client code's main function.
  Serializes argparse data to JSON for use with the Gooey front end
  '''

  params = locals()

  def build(payload):
    def inner():
      main_module_path = get_caller_path()
      _, filename = os.path.split(main_module_path)
      cleaned_source = clean_source(main_module_path)

      descriptor, tmp_filepath = tempfile.mkstemp(suffix='.py')
      atexit.register(cleanup, descriptor, tmp_filepath)

      with open(tmp_filepath, 'w') as f:
        f.write(cleaned_source)

      if not source_parser.has_argparse(cleaned_source):
        show_config = False

      build_spec = config_generator.create_from_module(tmp_filepath, **params)

      if dump_build_config:
        config_path = os.path.join(os.getcwd(), 'gooey_config.json')
        print 'Writing Build Config to: {}'.format(config_path)
        with open(config_path, 'w') as f:
          f.write(json.dumps(build_spec, indent=2))

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


def cleanup(descriptor, filepath):
  os.close(descriptor)
  os.remove(filepath)


if __name__ == '__main__':
  pass
