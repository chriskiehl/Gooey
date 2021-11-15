import json
import os
import signal
import sys
import textwrap
from argparse import ArgumentParser
from functools import wraps
from typing import List, Callable, Optional, Any

from gooey.python_bindings import signal_support
from gooey.gui.util.freeze import getResourcePath
from gooey.util.functional import merge
from python_bindings import constants
from python_bindings.gooey_decorator import gooey_params, IGNORE_COMMAND
from python_bindings.types import GooeyParams
from . import config_generator
from . import cmd_args




def Gooey1(f=None, **gkwargs):
    """TODO: explain the weirdness of decorators having different outputs"""
    params: GooeyParams = gooey_params(**gkwargs)

    @wraps(f)
    def inner(*args, **kwargs):
        parser_handler = choose_hander(params, sys.argv)
        # monkey patch parser
        ArgumentParser.original_parse_args = ArgumentParser.parse_args
        ArgumentParser.parse_args = parser_handler
        # return the wrapped, now monkey-patched, user function
        # to be later invoked
        return f(*args, **kwargs)

    def thunk(func):
        """
        Handles the case where the decorator is called
        with arguments (i.e. @Gooey(foo=bar) rather than @Gooey).
        TODO:
        """
        # type: ignore
        return Gooey1(func, **params)

    return inner if callable(f) else thunk



def bypass_gooey(params):
    """
    Bypasses all the Gooey machinery and runs the user's code directly.
    """
    def parse_args(self: ArgumentParser, args=None, namespace=None):
        # TODO: document that this is an experimental change
        # We previously mutated sys.argv directly to remove
        # the --ignore-gooey flag. But this caused lots of issues
        # See: https://github.com/chriskiehl/Gooey/issues/686
        # So, we instead modify the parser to transparently
        # consume the extra token
        self.add_argument('--ignore-gooey', action='store_true')
        args = self.original_parse_args(args, namespace)
        del args.ignore_gooey
        return args
    return parse_args


def validate_field(params):
    def parse_args(self: ArgumentParser, args=None, namespace=None):
        return None
    return parse_args


def valdiate_form(params):
    def parse_args(self: ArgumentParser, args=None, namespace=None):
        self.add_argument('--gooey-validate-form', action='store_true')
        args = self.original_parse_args(args, namespace)
        del args.gooey_validate_form
        print(json.dumps(vars(args)))
        sys.exit(80085)
    return parse_args


def handle_success(params):
    def parse_args(self: ArgumentParser, args=None, namespace=None):
        return None
    return parse_args


def handle_error(params):
    def parse_args(self: ArgumentParser, args=None, namespace=None):
        return None
    return parse_args


def handle_field_update(params):
    def parse_args(self: ArgumentParser, args=None, namespace=None):
        return None
    return parse_args


def handle_submit(params):
    def parse_args(self: ArgumentParser, args=None, namespace=None):
        return None
    return parse_args



def boostrap_gooey(params):
    """Bootstraps the Gooey UI."""
    def parse_args(self: ArgumentParser, args=None, namespace=None):
        # This import is delayed so it is not in the --ignore-gooey codepath.
        from gooey.gui import application
        source_path = sys.argv[0]

        build_spec = None
        if params['load_build_config']:
            try:
                exec_dir = os.path.dirname(sys.argv[0])
                open_path = os.path.join(exec_dir, params['load_build_config'])
                build_spec = json.load(open(open_path, "r"))
            except Exception as e:
                print('Exception loading Build Config from {0}: {1}'.format(params['load_build_config'], e))
                sys.exit(1)

        if not build_spec:
            if params['use_cmd_args']:
                cmd_args.parse_cmd_args(self, args)

            build_spec = config_generator.create_from_parser(
                self,
                source_path,
                **params)

        if params['dump_build_config']:
            config_path = os.path.join(os.path.dirname(sys.argv[0]), 'gooey_config.json')
            print('Writing Build Config to: {}'.format(config_path))
            with open(config_path, 'w') as f:
                f.write(json.dumps(build_spec, indent=2))
        application.run(build_spec)
    return parse_args



def choose_hander(params: GooeyParams, cliargs: List[str]):
    if '--gooey-validate-form' in cliargs:
        return valdiate_form(params)
    elif '--ignore-gooey' in cliargs:
        return bypass_gooey(params)
    else:
        return boostrap_gooey(params)



