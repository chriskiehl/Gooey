"""
All things Dynamic Updates & Validation.

Hear me all ye who enter!
=========================

This is a module of disgusting hacks and monkey patching. Control flow
is all over the place and a comprised of hodgepodge of various strategies.
This is all because Argparse's internal parsing design (a) really,
really, REALLY wants to fail and sys.exit at the first error it
finds, and (b) does these program ending validations at seemingly random
points throughout its code base. Meaning, there is no single centralized
validation module, class, or function which could be overridden in order to
achieve the desired behavior.

All that means is that it takes a fair amount of indirect, non-standard, and
gross monkey-patching to get Argparse to collect all its errors as it parses
rather than violently explode each time it finds one.

For additional background, see the original design here:
https://github.com/chriskiehl/Gooey/issues/755


"""
from argparse import ArgumentParser, _SubParsersAction, _MutuallyExclusiveGroup
from functools import wraps
from typing import Union, Any, Mapping, Dict, Callable

from gooey.python_bindings.types import Success, Failure, Try, InvalidChoiceException
from gooey.python_bindings.argparse_to_json import is_subparser
from gooey.util.functional import lift, identity, merge
from gooey.gui.constants import VALUE_PLACEHOLDER
from gooey.python_bindings.constants import Events
from gooey.python_bindings.coms import decode_payload
from gooey.gui.constants import RADIO_PLACEHOLDER

unexpected_exit_explanations = f'''
+=======================+
|Gooey Unexpected Error!|
+=======================+

Gooey encountered an unexpected error while trying to communicate 
with your program to process one of the {Events._fields} events.

These features are new and experimental! You may have encountered a bug! 

You can open a ticket with a small reproducible example here
https://github.com/chriskiehl/Gooey/issues
'''  # type: ignore


deserialize_failure_explanations = f'''
+==================================+
|Gooey Event Deserialization Error!|
+==================================+

Gooey was unable to deserialize the payload returned from your 
program when processing one of the {Events._fields} events. 

The payload *MUST* be in the `GooeyPublicState` schema. You can 
view the type information in `gooey.python_bindings.types.py`

Note, these features are new an experimental. This may be a bug on 
Gooey's side! 

You can open a ticket with a small reproducible example here:  
https://github.com/chriskiehl/Gooey/issues
'''


def check_value(registry: Dict[str, Exception], original_fn):
    """
    A Monkey Patch for `Argparse._check_value` which changes its
    behavior from one which throws an exception, to one which swallows
    the exception and silently records the failure.

    For certain argument types, Argparse calls a
    one-off `check_value` method. This method is inconvenient for us
    as it either returns nothing or throws an ArgumentException (thus leading
    to a sys.exit). Because our goal is to collect ALL
    errors for the entire parser, we must patch around this behavior.
    """
    @wraps(original_fn)
    def inner(self, action, value: Union[Any, Success, Failure]):
        def update_reg(_self, _action, _value):
            try:
                original_fn(_action, _value)
            except Exception as e:
                # check_value exclusively handles validating that the
                # supplied argument is a member of the `choices` set.
                # by default, it pops an exception containing all of the
                # available choices. However, since we're in a UI environment
                # all of that is redundant information. It's also *way too much*
                # information for things like FilterableDropdown. Thus we just
                # remap it to a 'simple' exception here.
                error = InvalidChoiceException("Selected option is not a valid choice")
                # IMPORTANT! note that this mutates the
                # reference that is passed in!
                registry[action.dest] = error

        # Inside of Argparse, `type_func` gets applied before the calls
        # to `check_value`. A such, depending on the type, this may already
        # be a lifted value.
        if isinstance(value, Success) and not isinstance(value, Failure):
            update_reg(self, action, value.value)
        elif isinstance(value, list) and all(x.isSuccess() for x in value):
            update_reg(self, action, [x.value for x in value])
        else:
            update_reg(self, action, value)
    return inner


def patch_args(*args, **kwargs):
    def inner(parser):
        return patch_argument(parser, *args, **kwargs)
    return inner

def patch_argument(parser, *args, **kwargs):
    """
    Mutates the supplied parser to append the arguments (args, kwargs) to
    the root parser and all subparsers.

    Example: `patch_argument(parser, '--ignore-gooey', action='store_true')

    This is used to punch additional cli arguments into the user's
    existing parser definition. By adding our arguments everywhere it allows
    us to use the `parse_args` machinery 'for free' without needing to
    worry about context shifts (like a repeated `dest` between subparsers).
    """
    parser.add_argument(*args, **kwargs)
    subparsers = list(filter(is_subparser, parser._actions))
    if subparsers:
        for sub in subparsers[0].choices.values():  # type: ignore
            patch_argument(sub, *args, **kwargs)
    return parser


def patch_all_parsers(patch_fn: Callable[[ArgumentParser], None], parser):
    subparsers = list(filter(is_subparser, parser._actions))
    if subparsers:
        for sub in subparsers[0].choices.values():  # type: ignore
            patch_all_parsers(patch_fn, sub)
    return parser


def recursively_patch_parser(parser, fn, *args):
    fn(parser, *args)
    subparsers = list(filter(is_subparser, parser._actions))
    if subparsers:
        for sub in subparsers[0].choices.values():  # type: ignore
            recursively_patch_parser(sub, fn, *args)
    return parser


def recursively_patch_actions(parser, fn):
    for action in parser._actions:
        if issubclass(type(action), _SubParsersAction):
            for subparser in action.choices.values():
                recursively_patch_actions(subparser, fn)
        else:
            fn(action)

def lift_action_type(action):
    """"""
    action.type = lift(action.type or identity)

def lift_actions_mutating(parser):
    """
    Mutates the supplied parser to lift all of its (likely) partial
    functions into total functions. See module docs for additional
    background. TL;DR: we have to "trick" Argparse into thinking
    every value is valid so that it doesn't short-circuit and sys.exit
    when it encounters a validation error. As such, we wrap everything
    in an Either/Try, and defer deciding the actual success/failure of
    the type transform until later in the execution when we have control.
    """
    recursively_patch_actions(parser, lift_action_type)
    # for action in parser._actions:
    #     if issubclass(type(action), _SubParsersAction):
    #         for subparser in action.choices.values():
    #             lift_actions_mutating(subparser)
    #     else:
    #         action.type = lift(action.type or identity)


def collect_errors(parser, error_registry: Dict[str, Exception], args: Dict[str, Try]) -> Dict[str, str]:
    """
    Merges all the errors from the Args mapping and error registry
    into a final dict.
    """
    # As is a theme throughout this module, to avoid Argparse
    # short-circuiting during parse-time, we pass a placeholder string
    # for required positional arguments which haven't yet been provided
    # by the user. So, what's happening here is that we're now collecting
    # all the args which have the placeholders so that we can flag them
    # all as required and missing.
    # Again, to be hyper clear, this is about being able to collect ALL
    # errors, versus just ONE error (Argparse default).
    required_but_missing = {k: 'This field is required'
                            for k, v in args.items()
                            if isinstance(v, Success) and v.value == VALUE_PLACEHOLDER}

    mutexes_required_but_missing = collect_mutex_errors(parser, args)

    errors = {k: str(v.error)
              for k, v in args.items()
              if v is not None and isinstance(v, Failure)}
    # Secondary errors are those which get frustratingly applied by
    # Argparse in a way which can't be easily tracked with patching
    # or higher order functions. See: `check_value` for more details.
    secondary = {k: str(e) for k, e in error_registry.items() if e}
    return merge(required_but_missing, errors, secondary, mutexes_required_but_missing)


def collect_mutex_errors(parser, args: Dict[str, Try]):
    """
    RadioGroups / MutuallyExclusiveGroup require extra care.
    Mutexes are not normal actions. They're not argument targets
    themselves, they have no `dest`, they're just parse-time containers
    for arguments. As such, there's no top-level argument destination
    we can tie a single error to. So, the strategy here is to mark _all_ of
    a radio group's children with an error if *any* of them are missing.

    It's a bit clunky, but what we've got to work with.
    """
    def dest_targets(group: _MutuallyExclusiveGroup):
        return [action.dest for action in group._group_actions]

    mutexes_missing = {dest for dest, v in args.items()
                     if isinstance(v, Success) and v.value == RADIO_PLACEHOLDER}

    return {dest: 'One of these must be provided'
            for group in parser._mutually_exclusive_groups
            for dest in dest_targets(group)
            # if the group is required and we've got one of its
            # children marked as missing
            if group.required and set(dest_targets(group)).intersection(mutexes_missing)}









def patch(obj, old_fn, new_fn):
    setattr(obj, old_fn, new_fn.__get__(obj, ArgumentParser))

def monkey_patch_check_value(parser, new_fn):
    parser._check_value = new_fn.__get__(parser, ArgumentParser)
    return parser

def monkey_patch(patcher, error_registry: Dict[str, Exception], parser):
    lift_actions_mutating(parser)
    patcher(parser)
    new_check_value = check_value(error_registry, parser._check_value)
    # https://stackoverflow.com/questions/28127874/monkey-patching-python-an-instance-method
    # parser._check_value = new_check_value.__get__(parser, ArgumentParser)

    return parser



def monkey_patch_for_form_validation(error_registry: Dict[str, Exception], parser):
    """
    Applies all the crufty monkey patching required to
    process a validate_form event
    """
    lift_actions_mutating(parser)
    patch_argument(parser, '--gooey-validate-form', action='store_true')
    patch_argument(parser, '--gooey-state', action='store', type=decode_payload)
    new_check_value = check_value(error_registry, parser._check_value)
    recursively_patch_parser(parser, monkey_patch_check_value, new_check_value)
    # https://stackoverflow.com/questions/28127874/monkey-patching-python-an-instance-method
    # patch(parser, '_check_value', new_check_value)
    # parser._check_value = new_check_value.__get__(parser, ArgumentParser)
    return monkey_patch_check_value(parser, new_check_value)

