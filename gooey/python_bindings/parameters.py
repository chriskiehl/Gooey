import signal
import sys
import textwrap

import os
from typing import List

from gooey.python_bindings.constants import Events
from gooey.python_bindings import constants
from gooey.gui.util.freeze import getResourcePath
from gooey.python_bindings.types import GooeyParams
from gooey.util.functional import merge



def _get_font_weight(kwargs):
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
    """
    Builds the full GooeyParams object from an arbitrary subset of supplied values
    """
    return GooeyParams(**{  # type: ignore
        'show_preview_warning': kwargs.get('show_preview_warning', True),
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

        'timing_options': merge({
            'show_time_remaining': False,
            'hide_time_remaining_on_complete': True
        }, kwargs.get('timing_options', {})),
        'disable_progress_bar_animation': kwargs.get('disable_progress_bar_animation', False),
        'disable_stop_button': kwargs.get('disable_stop_button'),
        'shutdown_signal': kwargs.get('shutdown_signal', signal.SIGTERM),
        'use_events': parse_events(kwargs.get('use_events', [])),


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
        'terminal_font_weight': _get_font_weight(kwargs),
        'terminal_font_size': kwargs.get('terminal_font_size', None),
        'richtext_controls': kwargs.get('richtext_controls', False),
        'error_color': kwargs.get('error_color', '#ea7878'),
        # TODO: remove. Only useful for testing
        'cli': kwargs.get('cli', sys.argv),
    })


def parse_events(events: List[str]) -> List[str]:
    if not isinstance(events, list):
        raise TypeError(
            f"`use_events` requires a list of events. You provided "
            "{events}. \n"
            "Example: \n"
            "\tfrom gooey import Events"
            "\t@Gooey(use_events=[Events.VALIDATE_FORM]")

    unknown_events = set(events) - set(Events)
    if unknown_events:
        raise ValueError(
            f'nrecognized event(s) were passed to `use_events`: {unknown_events}\n'
            f'Must be one of {Events._fields}\n'
            f'Consider using the `Events` object: `from gooey import Events`')
    else:
        return events
