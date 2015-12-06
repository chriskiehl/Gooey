import pytest
from gooey.python_bindings.argparse_to_json import *


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
  json_result = build_radio_group(exclusive_group)

  data = json_result['data'][0]
  assert 'RadioGroup' == json_result['type']
  assert target_arg.choices == data['choices']
  assert target_arg.help == data['help']
  assert target_arg.option_strings == data['commands']
  assert target_arg.dest == data['display_name']


def test_empty_mutex_group():
  assert not build_radio_group(None)


def test_as_json_invalid_widget():
  with pytest.raises(UnknownWidgetType):
    as_json(None, 'InvalidWidget', None)


def get_action(parser, dest):
  for action in parser._actions:
    if action.dest == dest:
      return action


def find_arg_by_option(group, option_string):
  for arg in group:
    if option_string in arg.option_strings:
      return arg
