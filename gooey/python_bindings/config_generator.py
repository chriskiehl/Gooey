import os
import sys
from gooey.gui.windows import layouts
from gooey.python_bindings import argparse_to_json
from gooey.gui.util.quoting import quote


def create_from_parser(parser, source_path, **kwargs):
  auto_start = kwargs.get('auto_start', False)

  run_cmd = kwargs.get('target')
  if run_cmd is None:
    if hasattr(sys, 'frozen'):
      run_cmd = quote(source_path)
    else:
      run_cmd = '{} -u {}'.format(quote(sys.executable), quote(source_path))

  build_spec = {
    'language':             kwargs.get('language', 'english'),
    'target':               run_cmd,
    'program_name':         kwargs.get('program_name') or os.path.basename(sys.argv[0]).replace('.py', ''),
    'program_description':  kwargs.get('program_description', ''),
    'auto_start':           kwargs.get('auto_start', False),
    'show_advanced':        kwargs.get('advanced', True),
    'default_size':         kwargs.get('default_size', (610, 530)),
    'num_required_cols':    kwargs.get('required_cols', 1),
    'num_optional_cols':    kwargs.get('optional_cols', 3),
    'manual_start':         False,
    'layout_type':          'flat',
    'monospace_display':    kwargs.get('monospace_display', False),
    'image_dir':            kwargs.get('image_dir'),
    'language_dir':         kwargs.get('language_dir'),
    'progress_regex':       kwargs.get('progress_regex'),
    'progress_expr':        kwargs.get('progress_expr'),
    'disable_progress_bar_animation': kwargs.get('disable_progress_bar_animation'),
    'disable_stop_button':  kwargs.get('disable_stop_button'),
    'group_by_type':        kwargs.get('group_by_type', True)
  }

  if not auto_start:
    build_spec['program_description'] = parser.description or build_spec['program_description']

    layout_data = argparse_to_json.convert(parser) if build_spec['show_advanced'] else layouts.basic_config.items()
    build_spec.update(layout_data)

  return build_spec
