import pytest
from gooey.python_bindings.argparse_to_json import *


@pytest.fixture
def empty_parser():
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
def subparser():
  parser = argparse.ArgumentParser(description='qidev')
  parser.add_argument('--verbose', help='be verbose', dest='verbose', action='store_true', default=False)
  subs = parser.add_subparsers(help='commands', dest='command')

  config_parser = subs.add_parser('config', help='configure defaults for qidev')
  config_parser.add_argument('field', help='the field to configure', type=str)
  config_parser.add_argument('value', help='set field to value', type=str)

  # ########################################################
  connect_parser = subs.add_parser('connect', help='connect to a robot (ip/hostname)')
  connect_parser.add_argument('hostname', help='hostname or IP address of the robot', type=str)

  # ########################################################
  install_parser = subs.add_parser('install', help='package and install a project directory on a robot')
  install_parser.add_argument('path', help='path to the project directory (containing manifest.xml', type=str)
  install_parser.add_argument('--ip', nargs='*', type=str, dest='ip', help='specify hostname(es)/IP address(es)')
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




def test_parser_converts_to_correct_type(empty_parser, complete_parser, subparser):
  assert convert(subparser)['layout_type'] == 'column'
  assert convert(empty_parser)['layout_type'] == 'standard'
  assert convert(complete_parser)['layout_type'] == 'standard'


def test_convert_std_parser(complete_parser):
  result = convert(complete_parser)
  assert result['layout_type'] == 'standard'
  assert result['widgets']
  assert isinstance(result['widgets'], list)

  entry = result['widgets'][0]
  assert 'type' in entry
  assert 'required' in entry
  assert 'data' in entry

  required = filter(lambda x: x['required'], result['widgets'])
  optional = filter(lambda x: not x['required'], result['widgets'])
  assert len(required) == 4
  assert len(optional) == 8


def test_convert_sub_parser(subparser):
  result = convert(subparser)
  assert result['layout_type'] == 'column'
  assert result['widgets']
  assert isinstance(result['widgets'], dict)
  assert len(result['widgets']) == 3


def test_has_required(empty_parser, complete_parser, subparser):
  assert has_required(complete_parser._actions)
  assert not has_required(empty_parser._actions)
  assert not has_required(subparser._actions)


def test_has_subparsers(subparser, complete_parser):
  assert has_subparsers(subparser._actions)
  assert not has_subparsers(complete_parser._actions)


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


def test_is_choice(empty_parser):
  empty_parser.add_argument('--dropdown', choices=[1,2])
  assert is_choice(get_action(empty_parser, 'dropdown'))

  empty_parser.add_argument('--storetrue', action='store_true')
  assert not is_choice(get_action(empty_parser, 'storetrue'))

  # make sure positionals are caught as well (issue #85)
  empty_parser.add_argument('positional', choices=[1, 2])
  assert is_choice(get_action(empty_parser, 'positional'))


def test_is_standard(empty_parser):
  empty_parser.add_argument('--count', action='count')
  assert not is_standard(get_action(empty_parser, 'count'))

  empty_parser.add_argument('--store', action='store')
  assert is_standard(get_action(empty_parser, 'store'))


def test_is_counter(empty_parser):
  empty_parser.add_argument('--count', action='count')
  assert is_counter(get_action(empty_parser, 'count'))

  empty_parser.add_argument('--dropdown', choices=[1,2])
  assert not is_counter(get_action(empty_parser, 'dropdown'))


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








