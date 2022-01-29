import os
import sys
import signal
import warnings
import textwrap
from gooey.python_bindings import argparse_to_json
from gooey.gui.util.quoting import quote
from gooey.python_bindings import constants
from gooey.python_bindings import gooey_decorator
from gooey.gui.util.functional import merge_dictionaries

default_layout = {
    'widgets': [{
      'type': 'CommandField',
      'required': True,
      'data': {
        'display_name': 'Enter Commands',
        'help': 'Enter command line arguments',
        'nargs': '',
        'commands': '',
        'choices': [],
        'default': None,
      }
    }],
}

# TODO: deprecate me
def create_from_parser(parser, source_path, **kwargs):

  run_cmd = kwargs.get('target')
  if run_cmd is None:
    if hasattr(sys, 'frozen'):
      run_cmd = quote(source_path)
    else:
      run_cmd = '{} -u {}'.format(quote(sys.executable), quote(source_path))

  build_spec = {**kwargs, 'target': run_cmd}

  if build_spec['monospace_display']:
      warnings.warn('Gooey Option `monospace_display` is a legacy option.\n'
                    'See the terminal_font_x options for more flexible control '
                    'over Gooey\'s text formatting')


  build_spec['program_description'] = build_spec['program_description'] or parser.description or ''

  layout_data = (argparse_to_json.convert(parser, **build_spec)
                   if build_spec['advanced']
                   else default_layout.items())

  build_spec.update(layout_data)

  if len(build_spec['widgets']) > 1:
    # there are subparsers involved
    build_spec['show_sidebar'] = True

  return build_spec



