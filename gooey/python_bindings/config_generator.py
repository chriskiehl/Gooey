import os
import sys
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


def create_from_parser(parser, source_path, **kwargs):

  run_cmd = kwargs.get('target')
  if run_cmd is None:
    if hasattr(sys, 'frozen'):
      run_cmd = quote(source_path)
    else:
      run_cmd = '{} -u {}'.format(quote(sys.executable), quote(source_path))

  build_spec = {
      'language':             kwargs.get('language', 'english'),
      'target':               run_cmd,
      # when running with a custom target, there is no need to inject
      # --ignore-gooey into the CLI args
      'suppress_gooey_flag':  kwargs.get('suppress_gooey_flag') or False,
      'program_name':         kwargs.get('program_name') or os.path.basename(sys.argv[0]).replace('.py', ''),
      'program_description':  kwargs.get('program_description') or '',
      'sidebar_title':        kwargs.get('sidebar_title', 'Actions'),
      'default_size':         kwargs.get('default_size', (610, 530)),
      'auto_start':           kwargs.get('auto_start', False),
      'show_advanced':        kwargs.get('advanced', True),
      'run_validators':       kwargs.get('run_validators', True),
      'encoding':             kwargs.get('encoding', 'utf-8'),
      'show_stop_warning':    kwargs.get('show_stop_warning', True),
      'show_success_modal':   kwargs.get('show_success_modal', True),
      'show_failure_modal':   kwargs.get('show_failure_modal', True),
      'force_stop_is_error':  kwargs.get('force_stop_is_error', True),
      'poll_external_updates':kwargs.get('poll_external_updates', False),
      'return_to_config':     kwargs.get('return_to_config', False),
      'show_restart_button':  kwargs.get('show_restart_button', True),
      'requires_shell':       kwargs.get('requires_shell', True),
      'menu':                 kwargs.get('menu', []),
      'clear_before_run':     kwargs.get('clear_before_run', False),
      'fullscreen':           kwargs.get('fullscreen', False),

      # Legacy/Backward compatibility interop
      'use_legacy_titles':    kwargs.get('use_legacy_titles', True),
      'num_required_cols':    kwargs.get('required_cols', 1),
      'num_optional_cols':    kwargs.get('optional_cols', 3),
      'manual_start':         False,
      'monospace_display':    kwargs.get('monospace_display', False),

      'image_dir':            kwargs.get('image_dir'),
      'language_dir':         kwargs.get('language_dir'),
      'progress_regex':       kwargs.get('progress_regex'),
      'progress_expr':        kwargs.get('progress_expr'),
      'hide_progress_msg':    kwargs.get('hide_progress_msg', False),
      'timing_options':       merge_dictionaries(gooey_decorator.defaults.get('timing_options'),kwargs.get('timing_options')),
      'disable_progress_bar_animation': kwargs.get('disable_progress_bar_animation'),
      'disable_stop_button':  kwargs.get('disable_stop_button'),

      # Layouts
      'navigation':           kwargs.get('navigation', constants.SIDEBAR),
      'show_sidebar':         kwargs.get('show_sidebar', False),
      'tabbed_groups':        kwargs.get('tabbed_groups', False),
      'group_by_type':        kwargs.get('group_by_type', True),

      # styles
      'body_bg_color':        kwargs.get('body_bg_color', '#f0f0f0'),
      'header_bg_color':      kwargs.get('header_bg_color', '#ffffff'),
      'header_height':        kwargs.get('header_height', 90),
      'header_show_title':    kwargs.get('header_show_title', True),
      'header_show_subtitle': kwargs.get('header_show_subtitle', True),
      'header_image_center':  kwargs.get('header_image_center', False),
      'footer_bg_color':      kwargs.get('footer_bg_color', '#f0f0f0'),
      'sidebar_bg_color':     kwargs.get('sidebar_bg_color', '#f2f2f2'),

      # font family, weight, and size are determined at runtime
      'terminal_panel_color': kwargs.get('terminal_panel_color', '#F0F0F0'),
      'terminal_font_color':  kwargs.get('terminal_font_color', '#000000'),
      'terminal_font_family': kwargs.get('terminal_font_family', None),
      'terminal_font_weight': get_font_weight(kwargs),
      'terminal_font_size':   kwargs.get('terminal_font_size', None),
      'richtext_controls':    kwargs.get('richtext_controls', False),
      'error_color':          kwargs.get('error_color', '#ea7878')
  }

  if build_spec['monospace_display']:
      warnings.warn('Gooey Option `monospace_display` is a legacy option.\n'
                    'See the terminal_font_x options for more flexible control '
                    'over Gooey\'s text formatting')


  build_spec['program_description'] = build_spec['program_description'] or parser.description or ''

  layout_data = (argparse_to_json.convert(parser, **build_spec)
                   if build_spec['show_advanced']
                   else default_layout.items())

  build_spec.update(layout_data)

  if len(build_spec['widgets']) > 1:
    # there are subparsers involved
    build_spec['show_sidebar'] = True

  return build_spec



def get_font_weight(kwargs):
    error_msg = textwrap.dedent('''
    Unknown font weight {}. 
    
    The available weights can be found in the `constants` module. 
    They're prefixed with "FONTWEIGHT" (e.g. `FONTWEIGHT_BOLD`)
    
    example code:    
    
    ```
    from gooey import constants
    @Gooey(terminal_font_weight=constants.FONTWEIGHT_NORMAL)
    ```   
    ''')
    weights = {
        constants.FONTWEIGHT_THIN,
        constants.FONTWEIGHT_EXTRALIGHT,
        constants.FONTWEIGHT_LIGHT,
        constants.FONTWEIGHT_NORMAL,
        constants.FONTWEIGHT_MEDIUM,
        constants.FONTWEIGHT_SEMIBOLD,
        constants.FONTWEIGHT_BOLD,
        constants.FONTWEIGHT_EXTRABOLD,
        constants.FONTWEIGHT_HEAVY,
        constants.FONTWEIGHT_EXTRAHEAVY
    }
    weight = kwargs.get('terminal_font_weight', constants.FONTWEIGHT_NORMAL)
    if weight not in weights:
        raise ValueError(error_msg.format(weight))
    return weight

