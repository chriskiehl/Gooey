"""
Converts argparse parser actions into json "Build Specs"
"""
import functools
import pprint
import argparse
import os
import sys
from argparse import (
    _CountAction,
    _HelpAction,
    _StoreConstAction,
    _StoreFalseAction,
    _StoreTrueAction,
    _SubParsersAction)
from collections import OrderedDict
from functools import partial
from uuid import uuid4

from gooey.util.functional import merge, getin

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
    'CheckBox',
    'MultiDirChooser',
    'Textarea',
    'PasswordField',
    'Listbox'
)


class UnknownWidgetType(Exception):
    pass


class UnsupportedConfiguration(Exception):
    pass



group_defaults = {
    'columns': 2,
    'padding': 10,
    'show_border': False
}

item_default = {
    'error_color': '#ea7878',
    'validator': {
        'type': 'local',
        'test': 'lambda x: True',
        'message': ''
    },
    'external_validator': {
        'cmd': '',
    }
}


def convert(parser, **kwargs):
    assert_subparser_constraints(parser)
    x = {
        'layout': 'standard',
        'widgets': OrderedDict(
            (choose_name(name, sub_parser), {
                'command': name,
                'contents': process(sub_parser,
                                    getattr(sub_parser, 'widgets', {}),
                                    getattr(sub_parser, 'options', {}))
            }) for name, sub_parser in iter_parsers(parser))
    }

    if kwargs.get('use_legacy_titles'):
        return apply_default_rewrites(x)
    return x


def process(parser, widget_dict, options):
    mutex_groups = parser._mutually_exclusive_groups
    raw_action_groups = [extract_groups(group) for group in parser._action_groups
                         if group._group_actions]
    corrected_action_groups = reapply_mutex_groups(mutex_groups, raw_action_groups)

    return categorize2(strip_empty(corrected_action_groups), widget_dict, options)

def strip_empty(groups):
    return [group for group in groups if group['items']]


def assert_subparser_constraints(parser):
    if has_subparsers(parser._actions):
        if has_required(parser._actions):
            raise UnsupportedConfiguration(
                "Gooey doesn't currently support top level required arguments "
                "when subparsers are present.")


def iter_parsers(parser):
    ''' Iterate over name, parser pairs '''
    try:
        return get_subparser(parser._actions).choices.items()
    except:
        return iter([('::gooey/default', parser)])


def extract_groups(action_group):
    '''
    Recursively extract argument groups and associated actions
    from ParserGroup objects
    '''
    return {
        'name': action_group.title,
        'description': action_group.description,
        'items': [action for action in action_group._group_actions
                  if not is_help_message(action)],
        'groups': [extract_groups(group)
                   for group in action_group._action_groups],
        'options': merge(group_defaults,
                               getattr(action_group, 'gooey_options', {}))
    }


def apply_default_rewrites(spec):
    top_level_subgroups = list(spec['widgets'].keys())

    for subgroup in top_level_subgroups:
        path = ['widgets', subgroup, 'contents']
        contents = getin(spec, path)
        for group in contents:
            if group['name'] == 'positional arguments':
                group['name'] = 'Required Arguments'
            if group['name'] == 'optional arguments':
                group['name'] = 'Optional Arguments'
    return spec


def contains_actions(a, b):
    ''' check if any actions(a) are present in actions(b) '''
    return set(a).intersection(set(b))


def reapply_mutex_groups(mutex_groups, action_groups):
    # argparse stores mutually exclusive groups independently
    # of all other groups. So, they must be manually re-combined
    # with the groups/subgroups to which they were originally declared
    # in order to have them appear in the correct location in the UI.
    #
    # Order is attempted to be preserved by inserting the MutexGroup
    # into the _actions list at the first occurrence of any item
    # where the two groups intersect
    def swap_actions(actions):
        for mutexgroup in mutex_groups:
            mutex_actions = mutexgroup._group_actions
            if contains_actions(mutex_actions, actions):
                # make a best guess as to where we should store the group
                targetindex = actions.index(mutexgroup._group_actions[0])
                # insert the _ArgumentGroup container
                actions[targetindex] = mutexgroup
                # remove the duplicated individual actions
                return [action for action in actions
                        if action not in mutex_actions]
        return actions

    return [group.update({'items': swap_actions(group['items'])}) or group
            for group in action_groups]


def categorize2(groups, widget_dict, options):
    return [{
        'name': group['name'],
        'items': list(categorize(group['items'], widget_dict, options)),
        'groups': categorize2(group['groups'], widget_dict, options),
        'description': group['description'],
        'options': group['options']
    } for group in groups]


def categorize(actions, widget_dict, options):
    _get_widget = partial(get_widget, widget_dict)
    for action in actions:

        if is_mutex(action):
            yield build_radio_group(action, widget_dict, options)

        elif is_standard(action):
            yield action_to_json(action, _get_widget(action, 'TextField'), options)

        elif is_choice(action):
            yield action_to_json(action, _get_widget(action, 'Dropdown'), options)

        elif is_flag(action):
            yield action_to_json(action, _get_widget(action, 'CheckBox'), options)

        elif is_counter(action):
            _json = action_to_json(action, _get_widget(action, 'Counter'), options)
            # pre-fill the 'counter' dropdown
            _json['data']['choices'] = list(map(str, range(1, 11)))
            yield _json
        else:
            raise UnknownWidgetType(action)


def get_widget(widgets, action, default):
    supplied_widget = widgets.get(action.dest, None)
    type_arg_widget = 'FileChooser' if action.type == argparse.FileType else None
    return supplied_widget or type_arg_widget or default


def is_required(action):
    '''
    _actions possessing the `required` flag and not implicitly optional
    through `nargs` being '*' or '?'
    '''
    return not isinstance(action, _SubParsersAction) and (
    action.required == True and action.nargs not in ['*', '?'])


def is_mutex(action):
    return isinstance(action, argparse._MutuallyExclusiveGroup)


def has_required(actions):
    return list(filter(None, list(filter(is_required, actions))))


def is_subparser(action):
    return isinstance(action, _SubParsersAction)


def has_subparsers(actions):
    return list(filter(is_subparser, actions))


def get_subparser(actions):
    return list(filter(is_subparser, actions))[0]


def is_optional(action):
    '''
    _actions either not possessing the `required` flag or implicitly optional
    through `nargs` being '*' or '?'
    '''
    return (not action.required) or action.nargs in ['*', '?']


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
    return any(list(map(lambda Action: isinstance(action, Action), action_types)))


def is_counter(action):
    """ _actions which are of type _CountAction """
    return isinstance(action, _CountAction)


def is_default_progname(name, subparser):
    return subparser.prog == '{} {}'.format(os.path.split(sys.argv[0])[-1], name)


def is_help_message(action):
    return isinstance(action, _HelpAction)


def choose_name(name, subparser):
    return name if is_default_progname(name, subparser) else subparser.prog


def build_radio_group(mutex_group, widget_group, options):
  return {
    'id': str(uuid4()),
    'type': 'RadioGroup',
    'cli_type': 'optional',
    'group_name': 'Choose Option',
    'required': mutex_group.required,
    'options': getattr(mutex_group, 'gooey_options', {}),
    'data': {
      'commands': [action.option_strings for action in mutex_group._group_actions],
      'widgets': list(categorize(mutex_group._group_actions, widget_group, options))
    }
  }


def action_to_json(action, widget, options):
    if action.required:
        # check that it's present and not just spaces
        validator = 'user_input and not user_input.isspace()'
        error_msg = 'This field is required'
    else:
        # not required; do nothing;
        validator = 'True'
        error_msg = ''

    base = merge(item_default, {
        'validator': {
            'test': validator,
            'message': error_msg
        },
    })

    return {
        'id': action.option_strings[0] if action.option_strings else action.dest,
        'type': widget,
        'cli_type': choose_cli_type(action),
        'required': action.required,
        'data': {
            'display_name': action.metavar or action.dest,
            'help': action.help,
            'required': action.required,
            'nargs': action.nargs or '',
            'commands': action.option_strings,
            'choices': action.choices or [],
            'default': clean_default(action.default),
            'dest': action.dest,
        },
        'options': merge(base, options.get(action.dest) or {})
    }


def choose_cli_type(action):
    return 'positional' \
            if action.required and not action.option_strings \
            else 'optional'

def clean_default(default):
    '''
    Attemps to safely coalesce the default value down to
    a valid JSON type.

    See: Issue #147.
    function references supplied as arguments to the
    `default` parameter in Argparse cause errors in Gooey.
    '''
    return default.__name__ if callable(default) else default
