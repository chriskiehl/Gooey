from itertools import chain

from gooey.gui.util import isOptional, isRequiredPositional
from gooey.gui.util import isRequiredNonPositional


def build_cmd_str(state, widgets):
    positional, required, optional = extractCmds(categorize_arguments(widgets))
    return finalize_command(state, positional, required, optional)


def categorize_arguments(widgets):
    return (
        filter(isRequiredPositional, widgets),
        filter(isRequiredNonPositional, widgets),
        filter(isOptional, widgets)
    )


def extractCmds(widgetGroups):
    return [[widget.get('cmd', None) for widget in group]
            for group in widgetGroups]


def finalize_command(state, positional, required, optional):
    if positional:
        positional.insert(0, "--")
    cmd_string = ' '.join(filter(None, chain(required, optional, positional)))

    if len(state['groups']) > 1:
        cmd_string = u'{} {}'.format(state['activeGroup']['command'], cmd_string)

    return u'{} --ignore-gooey {}'.format(state['target'], cmd_string)
