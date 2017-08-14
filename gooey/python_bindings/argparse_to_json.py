"""
Converts argparse parser actions into json "Build Specs"
"""

import argparse
import os
import sys
from _sha256 import sha256
from argparse import (
    _CountAction,
    _HelpAction,
    _StoreConstAction,
    _StoreFalseAction,
    _StoreTrueAction,
    _SubParsersAction)
from collections import defaultdict
from functools import reduce
from operator import itemgetter

from gooey.util import bootlegCurry, apply_transforms, merge, partition_by
from python_bindings.groupings import requiredAndOptional
from util import excluding, indentity


__ALL__ = (
    'convert',
    'UnknownWidgetType',
    'UnsupportedConfiguration'
)


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
    'PasswordField'
)


class UnknownWidgetType(Exception):
    pass


class UnsupportedConfiguration(Exception):
    pass




def convert(parser):
    '''
    Convert an ArgParse instance into a JSON representation for Gooey
    '''
    metadata = getattr(parser, 'metadata', {})
    toplevel_groups = get_toplevel_groups(parser)

    transforms = (
        flatten_actions,
        apply_identifiers,
        apply_gooey_metadata(metadata),
        clean_default_values,
        clean_types,
        make_json_friendly,
        group_mutex_groups,
        # requiredAndOptional
    )

    final_groups = []
    for group in toplevel_groups:
        final_groups.append(merge(
            excluding(group, 'parser'),
            {'items': reduce(apply_transforms, transforms, group['parser'])}
        ))

    return {
        'layout': 'column' if len(final_groups) > 1 else 'standard',
        'widgets': final_groups
    }




def fingerprint(obj):
    '''
    Generate a deterministic identifier for a given dict or object
    '''
    if isinstance(obj, dict):
        data = obj.items()
    else:
        data = obj.__dict__.items()
    hash = sha256(''.join(map(str, sorted(data))).encode('utf-8'))
    return hash.hexdigest()[:8]



def flatten_actions(parser):
    '''
    Turn all of the parser actions into a flattened list of dicts
    tagged with group and mutex info
    '''
    mutex_groups = {}
    for index, group in enumerate(parser._mutually_exclusive_groups):
        for action in group._group_actions:
            mutex_groups[fingerprint(action)] = group.title or index

    actions = []
    for index, group in enumerate(parser._action_groups):
        for order, action in enumerate(group._group_actions):
            hash = fingerprint(action)

            record = merge(action.__dict__, {
                'group_name': group.title or index,
                'mutex_group': mutex_groups.get(hash, None),
                'argparse_type': type(action),
                'order': order
            })
            actions.append(record)

    return actions


def apply_identifiers(actions):
    ''' Add a unique identifier to each action '''
    return [merge(action, {'id': fingerprint(action)}) for action in actions]


@bootlegCurry
def apply_gooey_metadata(metadata, actions):
    def add_metadata(metadata, action):
        '''
        Extends the action dict with widget, validatation,
        and any additional metadata required for the GUI
        '''
        widgets = metadata.get('widgets', {})
        validators = metadata.get('validators', {})

        defaults = (
            (is_standard, 'TextField', indentity),
            (is_choice, 'Dropdown', indentity),
            (is_flag, 'CheckBox', indentity),
            (is_counter, 'Counter', build_choice_array)
        )

        for predicate, default, finalizer in defaults:
            if predicate(action):
                widget = {'widget': get_widget(action, widgets) or default}
                validator = {'validator': get_validator(action, validators) or 'true'}
                return finalizer(merge(action, widget, validator))

        # if we fell out of the loop, a bad type was supplied by the user
        raise UnknownWidgetType(action)

    return [add_metadata(metadata, action) for action in actions]


def group_mutex_groups(actions):
    '''
    Wrap any mutexes up into their own sub-groups while taking
    special care to keep the ordering of the actions
    '''
    groups = defaultdict(list)

    for action in actions:
        groups[action['mutex_group']].append(action)

    output = []
    for mutex_name, stuff in groups.items():
        if mutex_name is not None:
            output.append({
                'name': mutex_name,
                'type': 'MutualExclusiveGroup',
                'items': stuff,
                'order': stuff[0]['order']
            })
        else:
            output.extend(stuff)

    return sorted(output, key=lambda x: x['order'])














def extract_subparser_details(parser):
    group_actions = parser._subparsers._group_actions[0]
    choice_actions = group_actions.choices.items()

    return [{
        'name': choose_name(name, item.parser),
        'command': name,
        'parser': item.parser
    } for name, item in choice_actions]


def clean_default_values(actions):
    return [merge(action, {
                'default': clean_default(action['argparse_type'], action['default'])
            }) for action in actions]


def clean_types(actions):
    ''' clean any user supplied type objects so they don't cause json explosions'''
    return [merge(action, {'type': action['type'].__name__ if callable(action['type']) else ''})
            for action in actions]


def wrap_parser(parser):
    '''
    Wrap a non-subparser ArgumentParser in
    a list of dicts to match the shape of subprocessor items
    '''
    return [{
        'name': 'primary',
        'command': None,
        'parser': parser
    }]


def get_toplevel_groups(parser):
    '''
    Get the top-level ArgumentParser groups/subparsers
    '''
    if parser._subparsers:
        return extract_subparser_details(parser)
    else:
        return wrap_parser(parser)


def make_json_friendly(actions):
    '''
    Remove any non-primitive argparse values from the dict
    that would cause serialization problems
    '''
    return [excluding(item, 'argparse_type', 'container') for item in actions]





def get_validator(action, validators):
    # TODO
    pass



def validate_subparser_constraints(parser):
    if parser._subparsers and has_required(parser._actions):
        raise UnsupportedConfiguration(
            "Gooey doesn't currently support required arguments when subparsers are present.")


def get_widget(action, widgets):
    supplied_widget = widgets.get(action['dest'], None)
    type_arg_widget = 'FileChooser' if action['type'] == argparse.FileType else None
    return supplied_widget or type_arg_widget or None





def has_required(actions):
    return list(filter(None, list(filter(is_required, actions))))


def is_required(action):
    '''
    _actions possessing the `required` flag and not implicitly optional
    through `nargs` being '*' or '?'
    '''
    return not isinstance(action, _SubParsersAction) and (
    action.required == True and action.nargs not in ['*', '?'])


def is_optional(action):
    '''
    _actions either not possessing the `required` flag or implicitly optional through `nargs` being '*' or '?'
    '''
    return (not action.required) or action.nargs in ['*', '?']


def is_choice(action):
    ''' action with choices supplied '''
    return action['choices']


def is_standard(action):
    '''
    actions which are general "store" instructions.
    e.g. anything which has an argument style like:
       $ script.py -f myfilename.txt
    '''
    boolean_actions = (
        _StoreConstAction, _StoreFalseAction,
        _StoreTrueAction
    )
    return (not action['choices']
            and not isinstance(action['argparse_type'], _CountAction)
            and not isinstance(action['argparse_type'], _HelpAction)
            and ['argparse_type'] not in boolean_actions)


def is_flag(action):
    ''' _actions which are either storeconst, store_bool, etc.. '''
    action_types = [_StoreTrueAction, _StoreFalseAction, _StoreConstAction]
    return any(list(map(lambda Action: isinstance(action, Action), action_types)))


def is_counter(action):
    """ _actions which are of type _CountAction """
    return isinstance(action, _CountAction)


def choose_name(name, subparser):
    return name if is_default_progname(name, subparser) else subparser.prog


def is_default_progname(name, subparser):
    return subparser.prog == '{} {}'.format(os.path.split(sys.argv[0])[-1], name)


def build_choice_array(action):
    ''' Generate a 1-10 choices array '''
    return merge(action, {'choices': list(map(str, range(1, 11)))})


def build_radio_group(mutex_group):
    if not mutex_group:
        return []

    options = [
        {
            'display_name': mutex_arg.metavar or mutex_arg.dest,
            'help': mutex_arg.help,
            'nargs': mutex_arg.nargs or '',
            'commands': mutex_arg.option_strings,
            'choices': mutex_arg.choices,
        } for mutex_arg in mutex_group
    ]

    return {
        'type': 'RadioGroup',
        'group_name': 'Choose Option',
        'required': False,
        'data': options
    }



def clean_default(widget_type, default):
    '''
    Attemps to safely coalesce the default value down to
    a valid JSON type.

    See: Issue #147.
    function references supplied as arguments to the
    `default` parameter in Argparse cause errors in Gooey.
    '''
    if widget_type != 'CheckBox':
        return default.__name__ if callable(default) else default
    # checkboxes must be handled differently, as they
    # must be forced down to a boolean value
    return default if isinstance(default, bool) else False



