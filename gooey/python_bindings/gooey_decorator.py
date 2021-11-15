'''
Created on Jan 24, 2014

@author: Chris

TODO: this
'''
import textwrap
from typing import Optional, Tuple, Union
import json
import os
import signal
import sys
from argparse import ArgumentParser

from typing_extensions import TypedDict, TypeAlias

from gooey.python_bindings import signal_support
from gooey.gui.util.freeze import getResourcePath
from gooey.util.functional import merge
from gooey.python_bindings import constants
from gooey.python_bindings.types import GooeyParams
from . import config_generator
from . import cmd_args





IGNORE_COMMAND = '--ignore-gooey'


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

# python can't type kwargs? wtf..
def gooey_params(**kwargs) -> GooeyParams:
    return GooeyParams(**{  # type: ignore
        'language': kwargs.get('language', 'english'),
        'target': kwargs.get('target'),

        'dump_build_config': kwargs.get('dump_build_config', False),
        'load_build_config': kwargs.get('load_build_config'),
        'use_cmd_args': kwargs.get('use_cmd_args', False),

        'suppress_gooey_flag': kwargs.get('suppress_gooey_flag') or False,
        # TODO: I should not read from the environment.
        # remains here for legacy reasons pending refactor
        'program_name': kwargs.get('program_name') or os.path.basename(sys.argv[0]).replace('.py', ''),
        'program_description': kwargs.get('program_description') or '',
        'sidebar_title': kwargs.get('sidebar_title', 'Actions'),
        'default_size': kwargs.get('default_size', (610, 530)),
        'auto_start': kwargs.get('auto_start', False),
        'advanced': kwargs.get('advanced', True),
        'run_validators': kwargs.get('run_validators', True),
        'encoding': kwargs.get('encoding', 'utf-8'),
        'show_stop_warning': kwargs.get('show_stop_warning', True),
        'show_success_modal': kwargs.get('show_success_modal', True),
        'show_failure_modal': kwargs.get('show_failure_modal', True),
        'force_stop_is_error': kwargs.get('force_stop_is_error', True),
        'poll_external_updates': kwargs.get('poll_external_updates', False),
        'return_to_config': kwargs.get('return_to_config', False),
        'show_restart_button': kwargs.get('show_restart_button', True),
        'requires_shell': kwargs.get('requires_shell', True),
        'menu': kwargs.get('menu', []),
        'clear_before_run': kwargs.get('clear_before_run', False),
        'fullscreen': kwargs.get('fullscreen', False),

        'use_legacy_titles': kwargs.get('use_legacy_titles', True),
        'required_cols': kwargs.get('required_cols', 2),
        'optional_cols': kwargs.get('optional_cols', 2),
        'manual_start': False,
        'monospace_display': kwargs.get('monospace_display', False),

        'image_dir': kwargs.get('image_dir', '::gooey/default'),
        # TODO: this directory resolution shouldn't happen here!
        # TODO: leaving due to legacy for now
        'language_dir': kwargs.get('language_dir', getResourcePath('languages')),
        'progress_regex': kwargs.get('progress_regex'),
        'progress_expr': kwargs.get('progress_expr'),
        'hide_progress_msg': kwargs.get('hide_progress_msg', False),

        'timing_options': kwargs.get('timing_options', {
            'show_time_remaining': False,
            'hide_time_remaining_on_complete': True
        }),
        'disable_progress_bar_animation': kwargs.get('disable_progress_bar_animation'),
        'disable_stop_button': kwargs.get('disable_stop_button'),
        'shutdown_signal': kwargs.get('shutdown_signal', signal.SIGTERM),


        'navigation': kwargs.get('navigation', constants.SIDEBAR),
        'show_sidebar': kwargs.get('show_sidebar', False),
        'tabbed_groups': kwargs.get('tabbed_groups', False),
        'group_by_type': kwargs.get('group_by_type', True),


        'body_bg_color': kwargs.get('body_bg_color', '#f0f0f0'),
        'header_bg_color': kwargs.get('header_bg_color', '#ffffff'),
        'header_height': kwargs.get('header_height', 90),
        'header_show_title': kwargs.get('header_show_title', True),
        'header_show_subtitle': kwargs.get('header_show_subtitle', True),
        'header_image_center': kwargs.get('header_image_center', False),
        'footer_bg_color': kwargs.get('footer_bg_color', '#f0f0f0'),
        'sidebar_bg_color': kwargs.get('sidebar_bg_color', '#f2f2f2'),


        'terminal_panel_color': kwargs.get('terminal_panel_color', '#F0F0F0'),
        'terminal_font_color': kwargs.get('terminal_font_color', '#000000'),
        'terminal_font_family': kwargs.get('terminal_font_family', None),
        'terminal_font_weight': get_font_weight(kwargs),
        'terminal_font_size': kwargs.get('terminal_font_size', None),
        'richtext_controls': kwargs.get('richtext_controls', False),
        'error_color': kwargs.get('error_color', '#ea7878')
    })



def Gooey2(f, **kwargs):
    params: GooeyParams = gooey_params(**kwargs)


def Gooey(f=None,
          advanced=True,
          language='english',
          auto_start=False,  # TODO: add this to the docs. Used to be `show_config=True`
          target=None,
          program_name=None,
          program_description=None,
          default_size=(610, 530),
          use_legacy_titles=True,
          required_cols=2,
          optional_cols=2,
          dump_build_config=False,
          load_build_config=None,
          monospace_display=False,  # TODO: add this to the docs
          image_dir='::gooey/default',
          language_dir=getResourcePath('languages'),
          progress_regex: Optional[str]=None,  # TODO: add this to the docs
          progress_expr: Optional[str]=None,  # TODO: add this to the docs
          hide_progress_msg=False,  # TODO: add this to the docs
          disable_progress_bar_animation=False,
          disable_stop_button=False,
          group_by_type=True,
          header_height=80,
          navigation='SIDEBAR', # TODO: add this to the docs
          tabbed_groups=False,
          use_cmd_args=False,
          **kwargs):
  '''
  Decorator for client code's main function.
  Serializes argparse data to JSON for use with the Gooey front end
  '''

  params = merge(locals(), locals()['kwargs'])

  if signal_support.requires_special_handler(sys.platform, params.get('shutdown_signal')):
    signal_support.install_handler()

  def build(payload):
    def run_gooey(self, args=None, namespace=None):
      # This import is delayed so it is not in the --ignore-gooey codepath.
      from gooey.gui import application
      source_path = sys.argv[0]

      build_spec = None
      if load_build_config:
        try:
          exec_dir = os.path.dirname(sys.argv[0])
          open_path = os.path.join(exec_dir,load_build_config)
          build_spec = json.load(open(open_path, "r"))
        except Exception as e:
          print('Exception loading Build Config from {0}: {1}'.format(load_build_config, e))
          sys.exit(1)

      if not build_spec:
        if use_cmd_args:
          cmd_args.parse_cmd_args(self, args)

        build_spec = config_generator.create_from_parser(
          self,
          source_path,
          payload_name=payload.__name__,
          **params)

      if dump_build_config:
        config_path = os.path.join(os.path.dirname(sys.argv[0]), 'gooey_config.json')
        print('Writing Build Config to: {}'.format(config_path))
        with open(config_path, 'w') as f:
          f.write(json.dumps(build_spec, indent=2))
      application.run(build_spec)

    def inner2(*args, **kwargs):
      ArgumentParser.original_parse_args = ArgumentParser.parse_args
      ArgumentParser.parse_args = run_gooey
      return payload(*args, **kwargs)

    inner2.__name__ = payload.__name__
    return inner2

  def run_without_gooey(func):
    return lambda *args, **kwargs: func(*args, **kwargs)

  if IGNORE_COMMAND in sys.argv:
    sys.argv.remove(IGNORE_COMMAND)
    if callable(f):
      return run_without_gooey(f)
    return run_without_gooey

  if callable(f):
    return build(f)
  return build


if __name__ == '__main__':
  pass
