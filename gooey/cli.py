'''The command line interface.'''

import sys
from importlib import import_module

from gooey import Gooey


def main(args=None):
    args = args or sys.argv[1:]
    module_path, function_name = args[0].split(':')
    if len(args) > 1:
        if args[1] == '--':
            del args[1]
    sys.argv = ['gooey', *args[1:]]
    module = import_module(module_path)
    function = getattr(module, function_name)
    return Gooey(function)()
