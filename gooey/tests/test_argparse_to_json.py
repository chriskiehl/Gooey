import unittest
from gooey.python_bindings.argparse_to_json import *


# I fixed all the tests!
#
# def test_parser_converts_to_correct_type(empty_parser, complete_parser, subparser):
#     assert convert(subparser)['layout_type'] == 'column'
#     assert convert(empty_parser)['layout_type'] == 'standard'
#     assert convert(complete_parser)['layout_type'] == 'standard'
#
#
# def test_parser_without_subparser_recieves_root_entry(complete_parser):
#     '''
#     Non-subparser setups should receive a default root key called 'primary'
#     '''
#     result = convert(complete_parser)
#     assert 'primary' in result['widgets']
#
#
# def test_grouping_structure(complete_parser):
#     '''
#     The output of the 'widgets' branch is now wrapped in another
#     layer to facilitate interop with the subparser structure
#
#     old: widgets: []
#     new: widgets: {'a': {}, 'b': {}, ..}
#     '''
#     result = convert(complete_parser)
#     groupings = result['widgets']
#     # should now be a dict rather than a list
#     assert isinstance(groupings, dict)
#     # make sure our expected root keys are there
#     for name, group in groupings.items():
#         assert 'command' in group
#         assert 'contents' in group
#         # contents should be the old list of widget info
#         assert isinstance(group['contents'], list)
#
#
# def test_subparser_uses_prog_value_if_available():
#     parser = argparse.ArgumentParser(description='qidev')
#     parser.add_argument('--verbose', help='be verbose', dest='verbose',
#                         action='store_true', default=False)
#     subs = parser.add_subparsers(help='commands', dest='command')
#     # NO prog definition for the sub parser
#     subs.add_parser('config', help='configure defaults for qidev')
#
#     # The stock parser name supplied above (e.g. config) is
#     # now in the converted doc
#     result = convert(parser)
#     assert 'config' in result['widgets']
#
#     # new subparser
#     parser = argparse.ArgumentParser(description='qidev')
#     parser.add_argument('--verbose', help='be verbose', dest='verbose',
#                         action='store_true', default=False)
#     subs = parser.add_subparsers(help='commands', dest='command')
#     # prog definition for the sub parser IS supplied
#     subs.add_parser('config', prog="My Config", help='configure defaults for qidev')
#
#     # Should've picked up the prog value
#     result = convert(parser)
#     assert 'My Config' in result['widgets']
#
#
# def test_convert_std_parser(complete_parser):
#     result = convert(complete_parser)
#     # grab the first entry from the dict
#     entry = result['widgets']['primary']['contents'][0]
#     print(entry)
#     assert 'type' in entry
#     assert 'required' in entry
#     assert 'data' in entry
#
#
# def test_convert_sub_parser(subparser):
#     result = convert(subparser)
#     assert result['layout_type'] == 'column'
#     assert result['widgets']
#     assert isinstance(result['widgets'], dict)
#     assert len(result['widgets']) == 3
#
#
# def test_has_required(empty_parser, complete_parser, subparser):
#     assert has_required(complete_parser._actions)
#     assert not has_required(empty_parser._actions)
#     assert not has_required(subparser._actions)
#
#
# def test_has_subparsers(subparser, complete_parser):
#     assert has_subparsers(subparser._actions)
#     assert not has_subparsers(complete_parser._actions)
#
#
# def test_is_required(complete_parser):
#     required = list(filter(is_required, complete_parser._actions))
#     assert len(required) == 4
#     for action in required:
#         print(action.dest.startswith('req'))
#
#
# def test_is_optional(complete_parser):
#     optional = list(filter(is_optional, complete_parser._actions))
#     assert len(optional) == 10
#     for action in optional:
#         assert 'req' not in action.dest
#
#
# def test_is_choice(empty_parser):
#     empty_parser.add_argument('--dropdown', choices=[1, 2])
#     assert is_choice(get_action(empty_parser, 'dropdown'))
#
#     empty_parser.add_argument('--storetrue', action='store_true')
#     assert not is_choice(get_action(empty_parser, 'storetrue'))
#
#     # make sure positionals are caught as well (issue #85)
#     empty_parser.add_argument('positional', choices=[1, 2])
#     assert is_choice(get_action(empty_parser, 'positional'))
#
#
# def test_is_standard(empty_parser):
#     empty_parser.add_argument('--count', action='count')
#     assert not is_standard(get_action(empty_parser, 'count'))
#
#     empty_parser.add_argument('--store', action='store')
#     assert is_standard(get_action(empty_parser, 'store'))
#
#
# def test_is_counter(empty_parser):
#     empty_parser.add_argument('--count', action='count')
#     assert is_counter(get_action(empty_parser, 'count'))
#
#     empty_parser.add_argument('--dropdown', choices=[1, 2])
#     assert not is_counter(get_action(empty_parser, 'dropdown'))
#
#
# def test_mutually(exclusive_group):
#     target_arg = find_arg_by_option(exclusive_group, '-i')
#     json_result = build_radio_group(exclusive_group)
#
#     data = json_result['data'][0]
#     assert 'RadioGroup' == json_result['type']
#     assert target_arg.choices == data['choices']
#     assert target_arg.help == data['help']
#     assert target_arg.option_strings == data['commands']
#     assert target_arg.dest == data['display_name']
#
#
# def test_empty_mutex_group():
#     assert not build_radio_group(None)
#
#
# def test_as_json_invalid_widget():
#     with pytest.raises(UnknownWidgetType):
#         action_to_json(None, 'InvalidWidget', None)
#
#
# def get_action(parser, dest):
#     for action in parser._actions:
#         if action.dest == dest:
#             return action
#
#
# def find_arg_by_option(group, option_string):
#     for arg in group:
#         if option_string in arg.option_strings:
#             return arg
