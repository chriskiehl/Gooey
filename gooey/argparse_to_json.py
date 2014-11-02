"""
Converts argparse parser actions into json "Build Specs"
"""

from argparse import (
  _CountAction,
  _HelpAction,
  _StoreConstAction,
  _StoreFalseAction,
  _StoreTrueAction
)
import itertools


VALID_WIDGETS = (
  '@FileChooser',
  '@DirChooser',
  '@DateChooser',
  '@TextField',
  '@Dropdown',
  '@Counter',
  '@RadioGroup'
)


def convert(argparser):


  mutually_exclusive_group = [
                  mutex_action
                  for group_actions in argparser._mutually_exclusive_groups
                  for mutex_action in group_actions._group_actions]

  base_actions = [action for action in argparser._actions
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
  filtered_actions = [action for action in actions
                     if not action.option_strings
                     or action.required == True]

  return [as_json(action, default_widget='TextField')
          for action in filtered_actions]


def get_optionals_with_choices(actions):
  """
  All optional arguments which are constrained
  to specific choices.
  """
  filtered_actions = [action
                      for action in actions
                      if action.choices]

  return [as_json(action, default_widget='Dropdown')
          for action in filtered_actions]


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
      action
      for action in actions
      if action.option_strings
      and not action.choices
      and not isinstance(action, _CountAction)
      and not isinstance(action, _HelpAction)
      and type(action) not in boolean_actions
  ]

  return [as_json(action, default_widget='TextField')
          for action in filtered_actions]


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
      action
      for action in actions
      if isinstance(action, _StoreTrueAction)
      or isinstance(action, _StoreFalseAction)
      or isinstance(action, _StoreConstAction)
  ]

  return [as_json(action, default_widget='CheckBox')
          for action in filtered_actions]


def get_counter_style_optionals(actions):
  """
  Returns all instances of type _CountAction
  """
  filtered_actions = [action
                      for action in actions
                      if isinstance(action, _CountAction)]

  _json_options =  [as_json(action, default_widget='Dropdown')
                    for action in filtered_actions]

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


def as_json(action, default_widget):
  option_strings = action.option_strings
  _type = option_strings[-1] if option_strings else None
  return {
    'type': widget_type(_type) if is_widget_spec(_type) else default_widget,
    'data' : {
      'display_name': action.dest,
      'help': action.help,
      'nargs': action.nargs or '',
      'commands': action.option_strings,
      'choices': action.choices or [],
    }
  }



def is_widget_spec(option_string):
  return option_string and option_string in VALID_WIDGETS

def widget_type(option_string):
  return option_string[1:]







