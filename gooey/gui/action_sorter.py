"""
Created on Dec 8, 2013

@author: Chris

"""

from argparse import (
  _CountAction,
  _HelpAction,
  _StoreConstAction,
  _StoreFalseAction,
  _StoreTrueAction
)


class ActionSorter(object):
  """
  Sorts all of the actions into their appropriate containers.

  Containers are based on the following map:

           COMPONENT MAP
       Action   		 WxWidget
    --------------------------
        store        TextCtrl
  store_const        CheckBox
   store_true        CheckBox
  store_False        CheckBox
       append        TextCtrl
        count 			 DropDown
       choice        DropDown

  Instance Variables:
    self._positionals
    self._choices
    self._optionals
    self._flags
    self._counters

  Example Argparse Def

  _HelpAction(option_strings=['-h', '--help'], dest='help', nargs=0, const=None, default='==SUPPRESS==', type=None, choices=None, help='show this help message and exit', metavar=None)
  _StoreAction(option_strings=[], dest='filename', nargs=None, const=None, default=None, type=None, choices=None, help='filename', metavar=None)
  _StoreTrueAction(option_strings=['-r', '--recursive'], dest='recurse', nargs=0, const=True, default=False, type=None, choices=None, help='recurse into subfolders [default: %(default)s]', metavar=None)
  _CountAction(option_strings=['-v', '--verbose'], dest='verbose', nargs=0, const=None, default=None, type=None, choices=None, help='set verbosity level [default: %(default)s]', metavar=None)
  _AppendAction(option_strings=['-i', '--include'], dest='include', nargs=None, const=None, default=None, type=None, choices=None, help='only include paths matching this regex pattern. Note: exclude is given preference over include. [default: %(default)s]', metavar='RE')
  _StoreAction(option_strings=['-e', '--exclude'], dest='exclude', nargs=None, const=None, default=None, type=None, choices=None, help='exclude paths matching this regex pattern. [default: %(default)s]', metavar='RE')
  _VersionAction(option_strings=['-V', '--version'], dest='version', nargs=0, const=None, default='==SUPPRESS==', type=None, choices=None, help="show program's version number and exit", metavar=None)
  _StoreAction(option_strings=['-T', '--tester'], dest='tester', nargs=None, const=None, default=None, type=None, choices=['yes', 'no'], help=None, metavar=None)
  _StoreAction(option_strings=[], dest='paths', nargs='+', const=None, default=None, type=None, choices=None, help='paths to folder(s) with source file(s) [default: %(default)s]', metavar='path')
  usage: example_argparse_souce.py [-h] [-r] [-v] [-i RE] [-e RE] [-V]
  """

  def __init__(self, actions):
    self._actions = actions[:]

    self._positionals = self.get_positionals(self._actions)
    self._choices = self.get_optionals_with_choices(self._actions)
    self._optionals = self.get_optionals_without_choices(self._actions)
    self._flags = self.get_flag_style_optionals(self._actions)
    self._counters = self.get_counter_actions(self._actions)

  def verbose(self):
    self._display('ActionSorter: positionals', self._positionals)
    self._display('ActionSorter: choices', self._choices)
    self._display('ActionSorter: optionals', self._optionals)
    self._display('ActionSorter: booleans', self._flags)
    self._display('ActionSorter: counters', self._counters)
    print '|-------------------------'

  def _display(self, _type, something):
    for i in something:
      print _type, i

  def get_counter_actions(self, actions):
    """
    Returns all instances of type _CountAction
    """
    return [action
            for action in actions
            if isinstance(action, _CountAction)]

  def get_positionals(self, actions):
    """
    Get all required (positional) actions
    """
    return [action
            for action in actions
            if not action.option_strings]

  def get_optionals_without_choices(self, actions):
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
    return [action
            for action in actions
            if action.option_strings
            and not action.choices
            and not isinstance(action, _CountAction)
            and not isinstance(action, _HelpAction)
            and type(action) not in boolean_actions]

  def get_optionals_with_choices(self, actions):
    """
    All optional arguments which are constrained
    to specific choices.
    """
    return [action
            for action in actions
            if action.choices]

  def get_flag_style_optionals(self, actions):
    """
    Gets all instances of "flag" type options.
    i.e. options which either store a const, or
    store boolean style options (e.g. StoreTrue).
    Types:
      _StoreTrueAction
      _StoreFalseAction
      _StoreConst
    """
    return [action
            for action in actions
            if isinstance(action, _StoreTrueAction)
            or isinstance(action, _StoreFalseAction)
            or isinstance(action, _StoreConstAction)]


if __name__ == '__main__':
  pass