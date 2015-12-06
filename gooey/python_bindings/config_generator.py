import os
import sys
from gooey.gui.windows import layouts
from gooey.python_bindings import argparse_to_json
from gooey.gui.util.quoting import quote


def create_from_parser(parser, source_path, **kwargs):
  show_config = kwargs.get('show_config', False)

  if hasattr(sys, 'frozen'):
    run_cmd = quote(source_path)
  else:
    run_cmd = '{} -u {}'.format(quote(sys.executable), quote(source_path))

  build_spec = {
    'language':             kwargs.get('language', 'english'),
    'target':               run_cmd,
    'program_name':         kwargs.get('program_name') or os.path.basename(sys.argv[0]).replace('.py', ''),
    'program_description':  kwargs.get('program_description', ''),
    'show_config':          show_config,
    'show_advanced':        kwargs.get('show_advanced', True),
    'default_size':         kwargs.get('default_size', (610, 530)),
    'num_required_cols':    kwargs.get('required_cols', 1),
    'num_optional_cols':    kwargs.get('optional_cols', 3),
    'manual_start':         False,
    'layout_type':          'column',
    'monospace_display':    kwargs.get('monospace_display', False),
    'image_dir':            kwargs.get('image_dir'),
    'language_dir':         kwargs.get('language_dir'),

  }

  if show_config:
    build_spec['program_description'] = parser.description or build_spec['program_description']

    layout_data = argparse_to_json.convert(parser) if build_spec['show_advanced'] else list(layouts.basic_config.items())
    build_spec.update(layout_data)

  else:
    build_spec['manual_start'] = True

  return build_spec
