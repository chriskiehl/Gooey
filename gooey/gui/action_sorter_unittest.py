"""
Created on Jan 16, 2014

@author: Chris
"""

import unittest
from argparse import _HelpAction

from action_sorter import ActionSorter
from gooey.gui import argparse_test_data


class TestActionSorter(unittest.TestCase):
  def setUp(self):
    self._actions = argparse_test_data.parser._actions
    self.sorted_actions = ActionSorter(self._actions)
    # pain in the A...
    self.expected_positionals = [
      "_StoreAction(option_strings=[], dest='filename', nargs=None, const=None, default=None, type=None, choices=None, help='Name of the file you want to read', metavar=None)",
      """_StoreAction(option_strings=[], dest='outfile', nargs=None, const=None, default=None, type=None, choices=None, help="Name of the file where you'll save the output", metavar=None)"""
    ]
    self.expected_choices = [
      """_StoreAction(option_strings=['-T', '--tester'], dest='tester', nargs=None, const=None, default=None, type=None, choices=['yes', 'no'], help="Yo, what's up man? I'm a help message!", metavar=None)"""
    ]
    self.expected_optionals = [
      """_StoreAction(option_strings=['-m', '--moutfile'], dest='moutfile', nargs=None, const=None, default=None, type=None, choices=None, help='Redirects output to the file specified by you, the awesome user', metavar=None)""",
      """_StoreAction(option_strings=['-v', '--verbose'], dest='verbose', nargs=None, const=None, default=None, type=None, choices=None, help='Toggles verbosity off', metavar=None)""",
      """_StoreAction(option_strings=['-s', '--schimzammy'], dest='schimzammy', nargs=None, const=None, default=None, type=None, choices=None, help='Add in an optional shimzammy parameter', metavar=None)"""
    ]
    self.expected_counters = [
      """_CountAction(option_strings=['-e', '--repeat'], dest='repeat', nargs=0, const=None, default=None, type=None, choices=None, help='Set the number of times to repeat', metavar=None)"""
    ]

    self.expected_flags = [
      """_StoreConstAction(option_strings=['-c', '--constoption'], dest='constoption', nargs=0, const='myconstant', default=None, type=None, choices=None, help='Make sure the const action is correctly sorted', metavar=None)""",
      """_StoreTrueAction(option_strings=['-t', '--truify'], dest='truify', nargs=0, const=True, default=False, type=None, choices=None, help='Ensure the store_true actions are sorted', metavar=None)""",
      """_StoreFalseAction(option_strings=['-f', '--falsificle'], dest='falsificle', nargs=0, const=False, default=True, type=None, choices=None, help='Ensure the store_false actions are sorted', metavar=None)"""
    ]

  def test_positionals_returns_only_positional_actions(self):
    positionals = self.sorted_actions._positionals
    self.assertEqual(len(positionals), 2)

    self.assert_for_all_actions_in_list(positionals, self.expected_positionals)

  def test_help_action_not_in_optionals(self):
    _isinstance = lambda x: isinstance(x, _HelpAction)
    self.assertFalse(any(map(_isinstance, self.sorted_actions._optionals)))

  def test_choices_only_returns_choices(self):
    self.assert_for_all_actions_in_list(self.sorted_actions._choices,
                                        self.expected_choices)

  def test_optionals_only_returns_optionals(self):
    self.assert_for_all_actions_in_list(self.sorted_actions._optionals,
                                        self.expected_optionals)

  def test_counter_sort_only_returns_counters(self):
    self.assert_for_all_actions_in_list(self.sorted_actions._counters,
                                        self.expected_counters)

  def test_flag_sort_returns_only_flags(self):
    self.assert_for_all_actions_in_list(self.sorted_actions._flags,
                                        self.expected_flags)

  def assert_for_all_actions_in_list(self, actions, expected_actions):
    for index, action in enumerate(actions):
      self.assertEqual(str(action), expected_actions[index])


if __name__ == "__main__":
  #import sys;sys.argv = ['', 'Test.testName']
  unittest.main()