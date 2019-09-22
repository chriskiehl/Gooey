from itertools import chain

from copy import deepcopy

from gooey.util.functional import compact


def buildCliString(target, cmd, positional, optional, suppress_gooey_flag=False):
    positionals = deepcopy(positional)
    if positionals:
        positionals.insert(0, "--")

    cmd_string = ' '.join(compact(chain(optional, positionals)))

    if cmd != '::gooey/default':
        cmd_string = u'{} {}'.format(cmd, cmd_string)

    ignore_flag = '' if suppress_gooey_flag else '--ignore-gooey'
    return u'{} {} {}'.format(target, ignore_flag, cmd_string)
