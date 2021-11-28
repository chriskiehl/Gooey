"""
Created on Jan 24, 2014  <-- so long ago!
"""
import sys
from argparse import ArgumentParser
from functools import wraps

from gooey.python_bindings.control import choose_hander
from gooey.python_bindings.parameters import gooey_params
from gooey.python_bindings.types import GooeyParams

IGNORE_COMMAND = '--ignore-gooey'


def Gooey(f=None, **gkwargs):
    """
    Decoration entry point for the Gooey process.
    See types.GooeyParams for kwargs options
    """
    params: GooeyParams = gooey_params(**gkwargs)

    @wraps(f)
    def inner(*args, **kwargs):
        parser_handler = choose_hander(params, gkwargs.get('cli', sys.argv))
        # monkey patch parser
        ArgumentParser.original_parse_args = ArgumentParser.parse_args
        ArgumentParser.parse_args = parser_handler
        # return the wrapped, now monkey-patched, user function
        # to be later invoked
        return f(*args, **kwargs)

    def thunk(func):
        """
        This just handles the case where the decorator is called
        with arguments (i.e. @Gooey(foo=bar) rather than @Gooey).

        Cause python is weird, when a decorator is called (e.g. @decorator())
        rather than just declared (e.g. @decorator), in complete and utter
        defiance of what your lying eyes see, it changes from a higher order
        function, to a function that takes an arbitrary argument *and then*
        returns a higher order function. i.e.

        decorate :: (a -> b) -> (a -> b)
        decorate() :: c -> (a -> b) -> (a -> b)

        wat.
        """
        return Gooey(func, **params)

    return inner if callable(f) else thunk

