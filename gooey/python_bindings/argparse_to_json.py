"""
Converts argparse parser actions into json "Build Specs"
"""

import argparse
from argparse import (
  _CountAction,
  _HelpAction,
  _StoreConstAction,
  _StoreFalseAction,
  _StoreTrueAction,
  ArgumentParser, _SubParsersAction)

from collections import OrderedDict
from functools import partial
from itertools import chain

VALID_WIDGETS = (
  'FileChooser',
  'MultiFileChooser',
  'FileSaver',
  'DirChooser',
  'DateChooser',
  'TextField',
  'Dropdown',
  'Counter',
  'RadioGroup',
  'CheckBox',
  'MultiDirChooser'
)


class UnknownWidgetType(Exception):
  pass

class UnsupportedConfiguration(Exception):
  pass


def convert(parser):
  widget_dict = getattr(parser, 'widgets', {})
  actions = parser._actions

  if has_subparsers(actions):
    if has_required(actions):
      raise UnsupportedConfiguration("Gooey doesn't currently support required arguments when subparsers are present.")
    layout_type = 'column'
    layout_data = {name.lower(): process(sub_parser, widget_dict) for name, sub_parser in get_subparser(actions).choices.iteritems()}
  else:
    layout_type = 'standard'
    layout_data = process(parser, widget_dict)

  return {
    'layout_type': layout_type,
    'widgets': layout_data
  }


def process(parser, widget_dict):
  mutually_exclusive_groups = [
                  [mutex_action for mutex_action in group_actions._group_actions]
                  for group_actions in parser._mutually_exclusive_groups]

  group_options = list(chain(*mutually_exclusive_groups))

  base_actions = [action for action in parser._actions
                  if action not in group_options
                  and action.dest != 'help']

  required_actions = filter(is_required, base_actions)
  optional_actions = filter(is_optional, base_actions)

  return list(categorize(required_actions, widget_dict, required=True)) + \
         list(categorize(optional_actions, widget_dict)) + \
         map(build_radio_group, mutually_exclusive_groups)

def categorize(actions, widget_dict, required=False):
  _get_widget = partial(get_widget, widgets=widget_dict)
  for action in actions:
    if is_standard(action):
      yield as_json(action, _get_widget(action) or 'TextField', required)
    elif is_choice(action):
      yield as_json(action, _get_widget(action) or 'Dropdown', required)
    elif is_flag(action):
      yield as_json(action, _get_widget(action) or 'CheckBox', required)
    elif is_counter(action):
      _json = as_json(action, _get_widget(action) or 'Dropdown', required)
      # pre-fill the 'counter' dropdown
      _json['data']['choices'] = map(str, range(1, 11))
      yield _json
    else:
      raise UnknownWidgetType(action)

def get_widget(action, widgets):
  supplied_widget = widgets.get(action.dest, None)
  type_arg_widget = 'FileChooser' if action.type == argparse.FileType else None
  return supplied_widget or type_arg_widget or None

def is_required(action):
  '''_actions which are positional or possessing the `required` flag '''
  return not action.option_strings and not isinstance(action, _SubParsersAction) or action.required == True

def has_required(actions):
  return filter(None, filter(is_required, actions))

def is_subparser(action):
  return isinstance(action,_SubParsersAction)

def has_subparsers(actions):
    return filter(is_subparser, actions)

def get_subparser(actions):
    return filter(is_subparser, actions)[0]

def is_optional(action):
  '''_actions not positional or possessing the `required` flag'''
  return action.option_strings and not action.required

def is_choice(action):
  ''' action with choices supplied '''
  return action.choices

def is_standard(action):
  """ actions which are general "store" instructions.
  e.g. anything which has an argument style like:
     $ script.py -f myfilename.txt
  """
  boolean_actions = (
    _StoreConstAction, _StoreFalseAction,
    _StoreTrueAction
  )
  return (not action.choices
          and not isinstance(action, _CountAction)
          and not isinstance(action, _HelpAction)
          and type(action) not in boolean_actions)

def is_flag(action):
  """ _actions which are either storeconst, store_bool, etc.. """
  action_types = [_StoreTrueAction, _StoreFalseAction, _StoreConstAction]
  return any(map(lambda Action: isinstance(action, Action), action_types))

def is_counter(action):
  """ _actions which are of type _CountAction """
  return isinstance(action, _CountAction)

def build_radio_group(mutex_group):
  if not mutex_group:
    return []

  options = [
    {
      'display_name': mutex_arg.dest,
      'help': mutex_arg.help,
      'nargs': mutex_arg.nargs or '',
      'commands': mutex_arg.option_strings,
      'choices': mutex_arg.choices,
    } for mutex_arg in mutex_group
  ]

  return {
    'type': 'RadioGroup',
    'group_name': 'Choose Option',
    'required': False,
    'data': options
  }


def as_json(action, widget, required):
  if widget not in VALID_WIDGETS:
    raise UnknownWidgetType('Widget Type {0} is unrecognized'.format(widget))

  return {
    'type': widget,
    'required': required,
    'data': {
      'display_name': action.dest,
      'help': action.help,
      'nargs': action.nargs or '',
      'commands': action.option_strings,
      'choices': action.choices or [],
      'default': action.default
    }
  }



