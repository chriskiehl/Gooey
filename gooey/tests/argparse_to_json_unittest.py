import argparse
import unittest
import json
from argparse_to_json import *

class TestArgparseToJson(unittest.TestCase):

  def setUp(self):
    my_cool_parser = argparse.ArgumentParser(description='description')
    my_cool_parser.add_argument("filename", help='filename help msg')  # positional
    my_cool_parser.add_argument("outfile", help="Name of the file where you'll save the output")  # positional
    my_cool_parser.add_argument('-c', '--countdown', default=10, type=int, help='sets the time to count down from')
    my_cool_parser.add_argument("-s", "--showtime", action="store_true", help="display the countdown timer")
    my_cool_parser.add_argument("-d", "--delay", action="store_true", help="Delay execution for a bit")
    my_cool_parser.add_argument('--verbose', '-v', action='count')
    my_cool_parser.add_argument("-o", "--obfuscate", action="store_true", help="obfuscate the countdown timer!")
    my_cool_parser.add_argument('-r', '--recursive', choices=['yes', 'no'], help='Recurse into subfolders')
    my_cool_parser.add_argument("-w", "--writelog", default="No, NOT whatevs", help="write log to some file or something")
    my_cool_parser.add_argument("-e", "--expandAll", action="store_true", help="expand all processes")
    verbosity = my_cool_parser.add_mutually_exclusive_group()
    verbosity.add_argument('-t', '--verboze', dest='verboze', action="store_true", help="Show more details")
    verbosity.add_argument('-q', '--quiet', dest='quiet', action="store_true", help="Only output on error")

    self.parser = my_cool_parser

    self.mutually_exclusive_group = [
                  mutex_action
                  for group_actions in self.parser._mutually_exclusive_groups
                  for mutex_action in group_actions._group_actions]

    self.base_actions = [action for action in self.parser._actions
                  if action not in self.mutually_exclusive_group]

  def test_get_optionals_with_choices(self):
    target_arg = self.find_arg_by_option(self.base_actions, '--recursive')
    json_result = get_optionals_with_choices(self.base_actions)
    self._test_parser_to_json_mapping(target_arg, json_result[0], 'Dropdown')

  def test_get_optionals_without_choices(self):
    target_arg = self.find_arg_by_option(self.base_actions, '--showtime')
    json_result = get_optionals_without_choices(self.base_actions)
    self._test_parser_to_json_mapping(target_arg, json_result[0], 'TextField')

  def test_get_counter_style_optionals(self):
    target_arg = self.find_arg_by_option(self.base_actions, '--verbose')
    json_result = get_counter_style_optionals(self.base_actions)
    print json_result
    self._test_parser_to_json_mapping(target_arg, json_result[0], 'Dropdown')

  def test_get_mutually_exclusive_optionals(self):
    target_arg = self.find_arg_by_option(self.mutually_exclusive_group, '--verboze')
    json_result = get_mutually_exclusive_optionals(self.mutually_exclusive_group)[0]
    data = json_result['data'][0]
    self.assertEqual('RadioGroup',              json_result['type'])
    self.assertEqual(target_arg.choices,        data['choices'])
    self.assertEqual(target_arg.help,           data['help'])
    self.assertEqual(target_arg.option_strings, data['commands'])
    self.assertEqual(target_arg.dest,           data['display_name'])


  def _test_parser_to_json_mapping(self, target_arg, json_string, expected_type):
    self.assertEqual(expected_type,             json_string['type'])
    self.assertEqual(target_arg.choices,        json_string['data']['choices'])
    self.assertEqual(target_arg.help,           json_string['data']['help'])
    self.assertEqual(target_arg.option_strings, json_string['data']['commands'])
    self.assertEqual(target_arg.dest,           json_string['data']['display_name'])


  def find_arg_by_option(self, group, option_string):
    for arg in group:
      if option_string in arg.option_strings:
        return arg


