import pytest
from gooey.python_bindings.argparse_to_json import *


@pytest.fixture
def parser():
  return argparse.ArgumentParser(description='description')

@pytest.fixture
def complete_parser():
  parser = argparse.ArgumentParser(description='description')
  parser.add_argument("req1", help='filename help msg')  # positional
  parser.add_argument("req2", help="Name of the file where you'll save the output")  # positional
  parser.add_argument('-r',   dest="req3", default=10, type=int, help='sets the time to count down from', required=True)
  parser.add_argument('--req4', dest="req4", default=10, type=int, help='sets the time to count down from', required=True)

  parser.add_argument("-a", "--aa", action="store_true", help="aaa")
  parser.add_argument("-b", "--bb", action="store_true", help="bbb")
  parser.add_argument('-c', '--cc', action='count')
  parser.add_argument("-d", "--dd", action="store_true", help="ddd")
  parser.add_argument('-e', '--ee', choices=['yes', 'no'], help='eee')
  parser.add_argument("-f", "--ff", default="0000", help="fff")
  parser.add_argument("-g", "--gg", action="store_true", help="ggg")
  verbosity = parser.add_mutually_exclusive_group()
  verbosity.add_argument('-i', '--ii', action="store_true", help="iii")
  verbosity.add_argument('-j', '--jj', action="store_true", help="hhh")
  return parser

@pytest.fixture
def exclusive_group():
  parser = argparse.ArgumentParser(description='description')
  verbosity = parser.add_mutually_exclusive_group()
  verbosity.add_argument('-i', dest="option1", action="store_true", help="iii")
  verbosity.add_argument('-j', dest="option2", action="store_true", help="hhh")

  mutually_exclusive_group = [mutex_action
                              for group_actions in parser._mutually_exclusive_groups
                              for mutex_action in group_actions._group_actions]
  return mutually_exclusive_group


def test_is_required(complete_parser):
  required = filter(is_required, complete_parser._actions)
  assert len(required) == 4
  for action in required:
    print action.dest.startswith('req')


def test_is_optional(complete_parser):
  optional = filter(is_optional, complete_parser._actions)
  assert len(optional) == 10
  for action in optional:
    assert 'req' not in action.dest


def test_is_choice(parser):
  parser.add_argument('--dropdown', choices=[1,2])
  assert is_choice(get_action(parser, 'dropdown'))

  parser.add_argument('--storetrue', action='store_true')
  assert not is_choice(get_action(parser, 'storetrue'))

  # make sure positionals are caught as well (issue #85)
  parser.add_argument('positional', choices=[1, 2])
  assert is_choice(get_action(parser, 'positional'))


def test_is_standard(parser):
  parser.add_argument('--count', action='count')
  assert not is_standard(get_action(parser, 'count'))

  parser.add_argument('--store', action='store')
  assert is_standard(get_action(parser, 'store'))

def test_is_counter(parser):
  parser.add_argument('--count', action='count')
  assert is_counter(get_action(parser, 'count'))

  parser.add_argument('--dropdown', choices=[1,2])
  assert not is_counter(get_action(parser, 'dropdown'))


def test_mutually(exclusive_group):
  target_arg = find_arg_by_option(exclusive_group, '-i')
  json_result = build_radio_group(exclusive_group)[0]

  data = json_result['data'][0]
  assert 'RadioGroup' == json_result['type']
  assert target_arg.choices == data['choices']
  assert target_arg.help == data['help']
  assert target_arg.option_strings == data['commands']
  assert target_arg.dest == data['display_name']


def get_action(parser, dest):
  for action in parser._actions:
    if action.dest == dest:
      return action

def find_arg_by_option(group, option_string):
  for arg in group:
    if option_string in arg.option_strings:
      return arg


