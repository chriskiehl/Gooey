"""
Converts argparse parser actions into json "Build Specs"
"""
import argparse
import json
import os
import sys
from argparse import (
    _CountAction,
    _HelpAction,
    _StoreConstAction,
    _StoreFalseAction,
    _StoreTrueAction,
    _StoreAction,
    _SubParsersAction,
    _VersionAction, _MutuallyExclusiveGroup)
from collections import OrderedDict
from functools import partial
from uuid import uuid4

from gooey.python_bindings.gooey_parser import GooeyParser
from gooey.util.functional import merge, getin, identity, assoc
from gooey.gui.components.options.validators import validators
from gooey.gui.components.options.validators import collect_errors

VALID_WIDGETS = (
    'FileChooser',
    'MultiFileChooser',
    'FileSaver',
    'DirChooser',
    'DateChooser',
    'TimeChooser',
    'TextField',
    'Dropdown',
    'Counter',
    'RadioGroup',
    'CheckBox',
    'BlockCheckbox',
    'MultiDirChooser',
    'Textarea',
    'PasswordField',
    'Listbox',
    'FilterableDropdown',
    'IntegerField',
    'DecimalField',
    'Slider'
)


# TODO: validate Listbox. When required, nargs must be +

class UnknownWidgetType(Exception):
    pass


class UnsupportedConfiguration(Exception):
    pass



# TODO: merge the default foreground and bg colors from the
# baseline build_spec
item_default = {
    'error_color': '#ea7878',
    'label_color': '#000000',
    'help_color': '#363636',
    'full_width': False,
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
    """
    Converts a parser into a JSON representation

    TODO:
    This is in desperate need of refactor. It wasn't build with supporting
    all (or any) of this configuration in mind. The use of global defaults
    are actively getting in the way of easily adding more configuration options.

    Pain points:
        - global data sprinkled throughout the calls
        - local data threaded through calls
        - totally unclear what the data structures even hold
        - everything is just mushed together and gross. unwinding argparse also
          builds validators, handles coercion, and so on...
        - converts to an entirely bespoke json mini-language that mirrors
          the internal structure of argparse.
    Refactor plan:
        - Investigate restructuring the core data representation. As is, it is ad-hoc
          and largely tied to argparse's goofy internal structure. May be worth moving to
          something "standard." Though, not sure what the options are.
        - standardize how these things read from the environment. No global in some local in others.
        - Investigate splitting the whole thing into phases (ala Ring). Current thinking is that
          a lot of this stuff could be modelled more like pluggable upgrades to the base structure.
        - I want to add a helpful validation stage to catch user errors like invalid gooey_options
    """

    group_defaults = {
        'legacy': {
            'required_cols': kwargs['required_cols'],
            'optional_cols': kwargs['optional_cols']
        },
        'columns': 2,
        'padding': 10,
        'show_border': False
    }

    assert_subparser_constraints(parser)
    x = {
        'layout': 'standard',
        'widgets': OrderedDict(
            (choose_name(name, sub_parser), {
                'command': name,
                'name': choose_name(name, sub_parser),
                'help': get_subparser_help(sub_parser),
                'description': '',
                'contents': process(sub_parser,
                                    getattr(sub_parser, 'widgets', {}),
                                    getattr(sub_parser, 'options', {}),
                                    group_defaults)
            }) for name, sub_parser in iter_parsers(parser))
    }

    if kwargs.get('use_legacy_titles'):
        return apply_default_rewrites(x)
    return x


def process(parser, widget_dict, options, group_defaults):
    mutex_groups = parser._mutually_exclusive_groups
    raw_action_groups = [extract_groups(group, group_defaults) for group in parser._action_groups
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


def get_subparser_help(parser):
    if isinstance(parser, GooeyParser):
        return getattr(parser.parser, 'usage', '')
    else:
        return getattr(parser, 'usage', '')


def extract_groups(action_group, group_defaults):
    '''
    Recursively extract argument groups and associated actions
    from ParserGroup objects
    '''
    return {
        'name': action_group.title,
        'description': action_group.description,
        'items': [action for action in action_group._group_actions
                  if not is_help_message(action)],
        'groups': [extract_groups(group, group_defaults)
                   for group in action_group._action_groups],
        'options': handle_option_merge(
            group_defaults,
            getattr(action_group, 'gooey_options', {}),
            action_group.title)
    }


def handle_option_merge(group_defaults, incoming_options, title):
    """
    Merges a set of group defaults with incoming options.

    A bunch of ceremony here is to ensure backwards compatibility with the old
    num_required_cols and num_optional_cols decorator args. They are used as
    the seed values for the new group defaults which keeps the old behavior
    _mostly_ in tact.

    Known failure points:
        * Using custom groups / names. No 'positional arguments' group
          means no required_cols arg being honored
        * Non-positional args marked as required. It would take group
          shuffling along the lines of that required to make
          mutually exclusive groups show in the correct place. In short, not
          worth the complexity for a legacy feature that's been succeeded by
          a much more powerful alternative.
    """
    if title == 'positional arguments':
        # the argparse default 'required' bucket
        req_cols = getin(group_defaults, ['legacy', 'required_cols'], 2)
        new_defaults = assoc(group_defaults, 'columns', req_cols)
        return merge(new_defaults, incoming_options)
    else:
        opt_cols = getin(group_defaults, ['legacy', 'optional_cols'], 2)
        new_defaults = assoc(group_defaults, 'columns', opt_cols)
        return merge(new_defaults, incoming_options)



def apply_default_rewrites(spec):
    top_level_subgroups = list(spec['widgets'].keys())

    for subgroup in top_level_subgroups:
        path = ['widgets', subgroup, 'contents']
        contents = getin(spec, path)
        for group in contents:
            if group['name'] == 'positional arguments':
                group['name'] = 'required_args_msg'
            if group['name'] == 'optional arguments':
                group['name'] = 'optional_args_msg'
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
                actions = [action for action in actions
                        if action not in mutex_actions]
        return actions

    return [group.update({'items': swap_actions(group['items'])}) or group
            for group in action_groups]


def categorize2(groups, widget_dict, options):
    defaults = {'label_color': '#000000', 'description_color': '#363636'}
    return [{
        'name': group['name'],
        'items': list(categorize(group['items'], widget_dict, options)),
        'groups': categorize2(group['groups'], widget_dict, options),
        'description': group['description'],
        'options': merge(defaults ,group['options'])
    } for group in groups]


def categorize(actions, widget_dict, options):
    _get_widget = partial(get_widget, widget_dict)
    for action in actions:
        if is_version(action):
            yield action_to_json(action, _get_widget(action, 'CheckBox'), options)

        elif is_mutex(action):
            yield build_radio_group(action, widget_dict, options)

        elif is_standard(action):
            yield action_to_json(action, _get_widget(action, 'TextField'), options)
        
        elif is_writemode_file(action):
            yield action_to_json(action, _get_widget(action, 'FileSaver'), options)

        elif is_readmode_file(action):
            yield action_to_json(action, _get_widget(action, 'FileChooser'), options)

        elif is_choice(action):
            yield action_to_json(action, _get_widget(action, 'Dropdown'), options)

        elif is_flag(action):
            yield action_to_json(action, _get_widget(action, 'CheckBox'), options)

        elif is_counter(action):
            _json = action_to_json(action, _get_widget(action, 'Counter'), options)
            # pre-fill the 'counter' dropdown
            _json['data']['choices'] = list(map(str, range(0, 11)))
            yield _json
        elif is_listbox(action):
            yield action_to_json(action, _get_widget(action, 'Listbox'), options)
        else:
            raise UnknownWidgetType(action)


def get_widget(widgets, action, default):
    supplied_widget = widgets.get(action.dest, None)
    return supplied_widget or default


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
    return action.choices and not action.nargs

def is_file(action):
    ''' action with FileType '''
    return isinstance(action.type, argparse.FileType)

def is_readmode_file(action):
    return is_file(action) and 'r' in action.type._mode

def is_writemode_file(action):
    # FileType uses the same modes as the builtin `open`
    # as such, all modes that aren't explicitly `r` (which is
    # also the default) are writable or read/writable, thus
    # making a FileChooser a good choice.
    return is_file(action) and 'r' not in action.type._mode

def is_version(action):
    return isinstance(action, _VersionAction) or issubclass(type(action), _VersionAction)


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
            and not isinstance(action.type, argparse.FileType)
            and not isinstance(action, (_CountAction, _HelpAction))
            # subclass checking is to handle the GooeyParser case
            # where Action get wrapped in a custom class
            and not issubclass(type(action), boolean_actions)
            and type(action) not in boolean_actions)


def is_flag(action):
    """ _actions which are either storeconst, store_bool, etc.. """
    # TODO: refactor to isinstance tuple form
    action_types = [_StoreTrueAction, _StoreFalseAction, _StoreConstAction]
    return (any(list(map(lambda Action: isinstance(action, Action), action_types)))
            or issubclass(type(action), (_StoreTrueAction, _StoreFalseAction, _StoreConstAction)))



def is_counter(action):
    """ _actions which are of type _CountAction """
    return isinstance(action, _CountAction)


def is_listbox(action):
    """ _actions whic can be translated into a Listbox """
    return (isinstance(action, _StoreAction)
            and action.choices
            and action.nargs in {'+', '*'})


def is_default_progname(name, subparser):
    return subparser.prog == '{} {}'.format(os.path.split(sys.argv[0])[-1], name)


def is_help_message(action):
    return isinstance(action, _HelpAction)


def choose_name(name, subparser):
    return name if is_default_progname(name, subparser) else subparser.prog


def build_radio_group(mutex_group, widget_group, options):
  dests = [action.dest for action in mutex_group._group_actions]
  return {
    'id': 'group_' + '_'.join(dests),
    'type': 'RadioGroup',
    'cli_type': 'optional',
    'group_name': 'Choose Option',
    'required': mutex_group.required,
    'options': merge(item_default, getattr(mutex_group, 'gooey_options', {})),
    'data': {
      'commands': [action.option_strings for action in mutex_group._group_actions],
      'widgets': list(categorize(mutex_group._group_actions, widget_group, options))
    }
  }


def action_to_json(action, widget, options):
    dropdown_types = {'Listbox', 'Dropdown', 'Counter'}
    if action.required:
        # Text fields get a default check that user input is present
        # and not just spaces, dropdown types get a simplified
        # is-it-present style check
        validator = ('user_input and not user_input.isspace()'
                     if widget not in dropdown_types
                     else 'user_input')
        error_msg = 'This field is required'
    else:
        # not required; do nothing;
        validator = 'True'
        error_msg = ''

    base = merge(item_default, {
        'validator': {
            'type': 'ExpressionValidator',
            'test': validator,
            'message': error_msg
        },
    })

    if (options.get(action.dest) or {}).get('initial_value') != None:
        value = options[action.dest]['initial_value']
        options[action.dest]['initial_value'] = handle_initial_values(action, widget, value)
    default = handle_initial_values(action, widget, action.default)
    if default == argparse.SUPPRESS:
        default = None



    final_options = merge(base, options.get(action.dest) or {})
    validate_gooey_options(action, widget, final_options)

    return {
        'id': action.dest,
        'type': widget,
        'cli_type': choose_cli_type(action),
        'required': action.required,
        'data': {
            'display_name': action.metavar or action.dest,
            'help': (action.help or '').replace('%%', '%'),
            'required': action.required,
            'nargs': action.nargs or '',
            'commands': action.option_strings,
            'choices': list(map(str, action.choices)) if action.choices else [],
            'default': default,
            'dest': action.dest,
        },
        'options': final_options
    }


def validate_gooey_options(action, widget, options):
    """Very basic field validation / sanity checking for
    the time being.

    Future plans are to assert against the options and actions together
    to facilitate checking that certain options like `initial_selection` in
    RadioGroups map to a value which actually exists (rather than exploding
    at runtime with an unhelpful error)

    Additional problems with the current approach is that no feedback is given
    as to WHERE the issue took place (in terms of stacktrace). Which means we should
    probably explode in GooeyParser proper rather than trying to collect all the errors here.
    It's not super ideal in that the user will need to run multiple times to
    see all the issues, but, ultimately probably less annoying that trying to
    debug which `gooey_option` key had an issue in a large program.

    That said "better is the enemy of done." This is good enough for now. It'll be
    a TODO: better validation 
    """
    errors = collect_errors(validators, options)
    if errors:
        from pprint import pformat
        raise ValueError(str(action.dest) + str(pformat(errors)))


def choose_cli_type(action):
    return 'positional' \
            if action.required and not action.option_strings \
            else 'optional'


def coerce_default(default, widget):
    """coerce a default value to the best appropriate type for
    ingestion into wx"""
    dispatcher = {
        'Listbox': clean_list_defaults,
        'Dropdown': safe_string,
        'Counter': safe_string
    }
    # Issue #321:
    # Defaults for choice types must be coerced to strings
    # to be able to match the stringified `choices` used by `wx.ComboBox`
    cleaned = clean_default(default)

    # dispatch to the appropriate cleaning function, or return the value
    # as is if no special handler is present
    return dispatcher.get(widget, identity)(cleaned)


def handle_initial_values(action, widget, value):
    handlers = [
        [textinput_with_nargs_and_list_default, coerse_nargs_list],
        [is_widget('Listbox'), clean_list_defaults],
        [is_widget('Dropdown'), coerce_str],
        [is_widget('Counter'), safe_string]
    ]
    for matches, apply_coercion in handlers:
        if matches(action, widget):
            return apply_coercion(value)
    return clean_default(value)


def coerse_nargs_list(default):
    """
    nargs=* and defaults which are collection types
    must be transformed into a CLI equivalent form. So, for
    instance, ['one two', 'three'] => "one two" "three"

    This only applies when the target widget is a text input. List
    based widgets such as Listbox should keep their defaults in list form

    Without this transformation, `add_arg('--foo', default=['a b'], nargs='*')` would show up in
    the UI as the literal string `['a b']` brackets and all.
    """
    return ' '.join('"{}"'.format(x) for x in default)

def is_widget(name):
    def equals(action, widget):
        return widget == name
    return equals


def textinput_with_nargs_and_list_default(action, widget):
    """
    Vanilla TextInputs which have nargs options which produce lists (i.e.
    nargs +, *, N, or REMAINDER) need to have their default values transformed
    into CLI style space-separated entries when they're supplied as a list of values
    on the Python side.
    """
    return (
        widget in {'TextField', 'Textarea', 'PasswordField'}
        and (isinstance(action.default, list) or isinstance(action.default, tuple))
        and is_list_based_nargs(action))


def is_list_based_nargs(action):
    """ """
    return isinstance(action.nargs, int) or action.nargs in {'*', '+', '...'}



def clean_list_defaults(default_values):
    """
    Listbox's default's can be passed as a single value
    or a collection of values (due to multiple selections). The list interface
    is standardized on for ease.
    """
    wrapped_values = ([default_values]
                      if isinstance(default_values, str)
                      else default_values)
    return [safe_string(value) for value in wrapped_values or []]


def clean_default(default):
    """
    Attempts to safely coalesce the default value down to
    a valid JSON type.
    """
    try:
        json.dumps(default)
        return default
    except TypeError as e:
        # see: Issue #377
        # if is isn't json serializable (i.e. primitive data) there's nothing
        # useful for Gooey to do with it (since Gooey deals in primitive data
        # types). So the correct behavior is dropping them. This affects ONLY
        # gooey, not the client code.
        return None


def safe_string(value):
    """
    Coerce a type to string as long as it isn't None or Boolean
    TODO: why do I have this special boolean case..?
    """
    if value is None or isinstance(value, bool):
        return value
    else:
        return str(value)


def coerce_str(value):
    """
    Coerce the incoming type to string as long as it isn't None
    """
    return str(value) if value is not None else value



def this_is_a_comment(action, widget):
    """
    TODO:
     - better handling of nargs.
     - allowing a class of "Narg'able" widget variants that allow dynamically adding options.
    Below are some rough notes on the current widgets and their nargs behavior (or lack of)
    """

    asdf = [
        # choosers are all currently treated as
        # singular inputs regardless of nargs status.
        'FileChooser',
        'MultiFileChooser',
        'FileSaver',
        'DirChooser',
        'DateChooser',
        'TimeChooser',

        # radiogroup requires no special logic. Delegates to internal widgets
        'RadioGroup',
        # nargs invalid
        'CheckBox',
        # nargs invalid
        'BlockCheckbox',

        # currently combines everything into a single, system _sep separated string
        # potential nargs behavior
        #   input: - each item gets a readonly textbox?
        #          - each item is its own editable widget?
        #          - problem with this idea is selected a ton of files would break the UI.
        #            maybe a better option would be to expose what's been added as a small
        #            list view? That way its a fixed size even if they choose 100s of files.
        #
        'MultiDirChooser',
        # special case. convert default to list of strings
        'Listbox',

        # special cases. coerce default to string
        'Dropdown',
        'Counter',

        # nargs behavior:
        #   - convert to space separated list of strings
        'TextField',
        'Textarea',
        'PasswordField',
    ]
