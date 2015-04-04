import os
import argparse_to_json
from gooey.gui.windows import layouts
from gooey.python_bindings import source_parser


def create_from_module(module_path, **kwargs):
  show_config = kwargs.get('show_config', False)

  run_cmd = 'python {}'.format(module_path)
  a = os.path.basename(module_path).replace('.py', '')
  build_spec = {
    'language':             kwargs.get('language', 'english'),
    'target':               run_cmd,
    'program_name':         kwargs.get('program_name') or os.path.basename(module_path).replace('.py', ''),
    'program_description':  kwargs.get('program_description', ''),
    'show_config':          show_config,
    'show_advanced':        kwargs.get('show_advanced', True),
    'default_size':         kwargs.get('default_size', (610, 530)),
    'requireds_cols':       kwargs.get('required_cols', 1),
    'optionals_cols':       kwargs.get('optional_cols', 3),
    'manual_start':         False
  }

  if show_config:
    parser = source_parser.extract_parser(module_path)
    build_spec['program_description'] = parser.description or build_spec['program_description']

    layout_data = argparse_to_json.convert(parser) if build_spec['show_advanced'] else layouts.basic_config.items()
    build_spec.update(layout_data)

  else:
    build_spec['manual_start'] = True

  return build_spec



def has_argparse(module_path):
  return any(['.parse_args(' in line.lower() for line in f.readlines()])
