"""
Converts argparse parser actions into json "Build Specs"
"""

from argparse import (
  _CountAction,
  _HelpAction,
  _StoreConstAction,
  _StoreFalseAction,
  _StoreTrueAction,
  ArgumentParser)
import itertools


VALID_WIDGETS = (
  'FileChooser',
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


  base_actions = [(action, widget_dict.get(action.dest, None))
                  for action in parser._actions
                  if action not in mutually_exclusive_group]



  positional_args = get_required_and_positional_args(base_actions)

  choice_args     = get_optionals_with_choices(base_actions)
  standard_args   = get_optionals_without_choices(base_actions)
  counter_args    = get_counter_style_optionals(base_actions)
  radio_args      = get_mutually_exclusive_optionals(mutually_exclusive_group)
  checkable_args  = get_flag_style_optionals(base_actions)

  return {
    'required': positional_args,
    'optional': list(itertools.chain(
      get_optionals_with_choices(base_actions),
      get_optionals_without_choices(base_actions),
      get_counter_style_optionals(base_actions),
      get_mutually_exclusive_optionals(mutually_exclusive_group),
      get_flag_style_optionals(base_actions)
    )),
  }





def get_required_and_positional_args(actions):
  """
  Extracts positional or required args from the actions list
  In argparse, positionals are defined by either an empty option_strings
  or by the option_strings parameters being sans a leading hyphen
  """
  filtered_actions = [(action, widget)
                      for action, widget in actions
                      if not action.option_strings
                      or action.required == True]

  return [as_json(action, widget=widget or 'TextField')
          for action, widget in filtered_actions]


def get_optionals_with_choices(actions):
  """
  All optional arguments which are constrained
  to specific choices.
  """
  filtered_actions = [(action, widget)
                      for action, widget in actions
                      if action.choices]

  return [as_json(action, widget=widget or 'Dropdown')
          for action, widget in filtered_actions]


def get_optionals_without_choices(actions):
  """
  All actions which are:
    (a) Optional, but without required choices
    (b) Not of a "boolean" type (storeTrue, etc..)
    (c) Of type _AppendAction

  e.g. anything which has an argument style like:
     >>>	-f myfilename.txt
  """
  boolean_actions = (
    _StoreConstAction, _StoreFalseAction,
    _StoreTrueAction
  )
  filtered_actions = [
      (action, widget)
      for action, widget in actions
      if action.option_strings
      and not action.choices
      and not isinstance(action, _CountAction)
      and not isinstance(action, _HelpAction)
      and type(action) not in boolean_actions
  ]

  return [as_json(action, widget=widget or 'TextField')
          for action, widget in filtered_actions]


def get_flag_style_optionals(actions):
  """
  Gets all instances of "flag" type options.
  i.e. options which either store a const, or
  store boolean style options (e.g. StoreTrue).
  Types:
    _StoreTrueAction
    _StoreFalseAction
    _StoreConst
  """
  filtered_actions = [
      (action, widget)
      for action, widget in actions
      if isinstance(action, _StoreTrueAction)
      or isinstance(action, _StoreFalseAction)
      or isinstance(action, _StoreConstAction)
  ]

  return [as_json(action, widget=widget or 'CheckBox')
          for action, widget in filtered_actions]


def get_counter_style_optionals(actions):
  """
  Returns all instances of type _CountAction
  """
  filtered_actions = [(action, widget)
                      for action, widget in actions
                      if isinstance(action, _CountAction)]

  _json_options =  [as_json(action, widget=widget or 'Counter')
                    for action, widget in filtered_actions]

  # Counter should show as Dropdowns, so pre-populare with numeric choices
  for opt in _json_options:
    opt['choices'] = range(10)
  return _json_options


def get_mutually_exclusive_optionals(mutex_group):
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




