from itertools import chain

from copy import deepcopy

from gooey.util.functional import compact


def buildCliString(target, cmd, positional, optional):
    positionals = deepcopy(positional)
    if positionals:
        positionals.insert(0, "--")

    cmd_string = ' '.join(compact(chain(optional, positionals)))

    if cmd != '::gooey/default':
        cmd_string = u'{} {}'.format(cmd, cmd_string)

    return u'{} --ignore-gooey {}'.format(target, cmd_string)
