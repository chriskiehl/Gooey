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
  ArgumentParser)


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
  'CheckBox'
)


class UnknownWidgetType(Exception):
  pass


def convert(parser):
  widget_dict = getattr(parser, 'widgets', {})

  mutually_exclusive_group = [
                  mutex_action
                  for group_actions in parser._mutually_exclusive_groups
                  for mutex_action in group_actions._group_actions]


  base_actions = [action for action in parser._actions
                  if action not in mutually_exclusive_group
                  and action.dest != 'help']

  required_actions = filter(is_required, base_actions)
  optional_actions = filter(is_optional, base_actions)

  return {
    'required': list(categorize(required_actions, widget_dict)),
    'optional': list(categorize(optional_actions, widget_dict)) + build_radio_group(mutually_exclusive_group)
  }

def categorize(actions, widget_dict):
  for action in actions:
    if is_standard(action):
      yield as_json(action, get_widget(action, widget_dict) or 'TextField')
    elif is_choice(action):
      yield as_json(action, get_widget(action, widget_dict) or 'Dropdown')
    elif is_counter(action):
      _json = as_json(action, get_widget(action, widget_dict) or 'Dropdown')
      # prefill the 'counter' dropdown
      _json['choices'] = range(1, 11)
      yield _json
    elif is_flag(action):
      yield as_json(action, get_widget(action, widget_dict) or 'CheckBox')
    else:
      raise UnknownWidgetType(action)

def get_widget(action, widgets):
  supplied_widget = widgets.get(action.dest, None)
  type_arg_widget = 'FileChooser' if action.type == argparse.FileType else None
  return supplied_widget or type_arg_widget or None

def is_required(action):
  '''_actions which are positional or possessing the `required` flag '''
  return not action.option_strings or action.required == True

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

  return [{
    'type': 'RadioGroup',
    'group_name': 'Choose Option',
    'data': options
  }]


def as_json(action, widget):
  if widget not in VALID_WIDGETS:
    raise UnknownWidgetType('Widget Type {0} is unrecognized'.format(widget))

  option_strings = action.option_strings
  return {
    'type': widget,
    'data': {
      'display_name': action.dest,
      'help': action.help,
      'nargs': action.nargs or '',
      'commands': action.option_strings,
      'choices': action.choices or [],
    }
  }




