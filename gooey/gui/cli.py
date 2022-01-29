import json
from itertools import chain

from copy import deepcopy

from gooey.util.functional import compact
from typing import List, Optional

from gooey.gui.constants import VALUE_PLACEHOLDER
from gooey.gui.formatters import formatArgument
from gooey.python_bindings.types import FieldValue, Group, Item
from gooey.util.functional import merge  # type: ignore
from gooey.gui.state import FullGooeyState

'''
primary :: Target -> Command -> Array Arg -> Array Arg -> Boolean -> CliString
validateForm :: Target -> Command -> Array Arg -> Array Arg -> CliString
validateField :: Target -> Command -> Array Arg -> Array Arg -> ArgId -> CliString
completed :: Target -> Command -> FromState -> CliString
failed :: Target -> Command -> FromState -> CliString
fieldAction :: Target -> Command ->   

'''


def buildSuccessCmd(state: FullGooeyState):
    subcommand = state['subcommands'][state['activeSelection']]
    widgets = state['widgets'][subcommand]




def onSuccessCmd(target: str, subCommand: str, formState: List[str]) -> str:
    command = subCommand if not subCommand == '::gooey/default' else ''
    return f'{target} {command} --gooey-on-success {json.dumps(formState)}'


def onErrorCmd(target: str, subCommand: str, formState: List[str]) -> str:
    command = subCommand if not subCommand == '::gooey/default' else ''
    return f'{target} {command} --gooey-on-error {json.dumps(formState)}'


def formValidationCmd(target: str, subCommand: str, positionals: List[FieldValue], optionals: List[FieldValue]) -> str:
    positional_args = [cmdOrPlaceholderOrNone(x) for x in positionals]
    optional_args = [cmdOrPlaceholderOrNone(x) for x in optionals]
    command = subCommand if not subCommand == '::gooey/default' else ''
    return u' '.join(compact([
        target,
        command,
        *optional_args,
        '--gooey-validate-form',
        '--' if positional_args else '',
        *positional_args]))


def cliCmd(target: str,
           subCommand: str,
           positionals: List[FieldValue],
           optionals: List[FieldValue],
           suppress_gooey_flag=False) -> str:
    positional_args = [arg['cmd'] for arg in positionals]
    optional_args = [arg['cmd'] for arg in optionals]
    command = subCommand if not subCommand == '::gooey/default' else ''
    ignore_flag = '' if suppress_gooey_flag else '--ignore-gooey'
    return u' '.join(compact([
        target,
        command,
        *optional_args,
        ignore_flag,
        '--' if positional_args else '',
        *positional_args]))


def cmdOrPlaceholderOrNone(field: FieldValue) -> Optional[str]:
    # Argparse has a fail-fast-and-exit behavior for any missing
    # values. This poses a problem for dynamic validation, as we
    # want to collect _all_ errors to be more useful to the user.
    # As such, if there is no value currently available, we pass
    # through a stock placeholder values which allows GooeyParser
    # to handle it being missing without Argparse exploding due to
    # it actually being missing.
    if field['clitype'] == 'positional':
        return field['cmd'] or VALUE_PLACEHOLDER
    elif field['clitype'] != 'positional' and field['meta']['required']:
        # same rationale applies here. We supply the argument
        # along with a fixed placeholder (when relevant i.e. `store`
        # actions)
        return field['cmd'] or formatArgument(field['meta'], VALUE_PLACEHOLDER)
    else:
        # Optional values are, well, optional. So, like usual, we send
        # them if present or drop them if not.
        return field['cmd']


def buildCliString(target, subCommand, positional, optional, suppress_gooey_flag=False):
    positionals = deepcopy(positional)
    if positionals:
        positionals.insert(0, "--")

    arguments = ' '.join(compact(chain(optional, positionals)))

    if subCommand != '::gooey/default':
        arguments = u'{} {}'.format(subCommand, arguments)

    ignore_flag = '' if suppress_gooey_flag else '--ignore-gooey'
    return u'{} {} {}'.format(target, ignore_flag, arguments)
