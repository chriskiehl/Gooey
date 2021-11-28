import json
import os
import sys
from argparse import ArgumentParser
from typing import List, Dict

from gooey.python_bindings.dynamics import monkey_patch_for_form_validation
from gooey.python_bindings.dynamics import patch_argument, collect_errors
from gooey.python_bindings.types import GooeyParams
from . import cmd_args
from . import config_generator


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
        # consume the extra token.
        patched_parser = patch_argument(self, '--ignore-gooey', action='store_true')
        args = patched_parser.original_parse_args(args, namespace)  # type: ignore
        # removed from the arg object so the user doesn't have
        # to deal with it or be confused by it
        del args.ignore_gooey
        return args
    return parse_args


def validate_form(params: GooeyParams, write=print, exit=sys.exit):
    """
    Validates the user's current form.
    """
    def parse_args(self: ArgumentParser, args=None, namespace=None):
        error_registry: Dict[str, Exception] = {}
        patched_parser = monkey_patch_for_form_validation(error_registry, self)
        try:
            args = patched_parser.original_parse_args(args, namespace)  # type: ignore
            errors = collect_errors(error_registry, vars(args))
            write(json.dumps(errors))
            exit(0)
        except Exception as e:
            write(e)
            exit(1)
    return parse_args


def boostrap_gooey(params: GooeyParams):
    """Bootstraps the Gooey UI."""
    def parse_args(self: ArgumentParser, args=None, namespace=None):
        # This import is delayed so it is not in the --ignore-gooey codepath.
        from gooey.gui import application
        source_path = sys.argv[0]

        build_spec = None
        if params['load_build_config']:
            try:
                exec_dir = os.path.dirname(sys.argv[0])
                open_path = os.path.join(exec_dir, params['load_build_config'])  # type: ignore
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



def validate_field(params):
    def parse_args(self: ArgumentParser, args=None, namespace=None):
        raise NotImplementedError
    return parse_args


def handle_success(params):
    def parse_args(self: ArgumentParser, args=None, namespace=None):
        raise NotImplementedError
    return parse_args


def handle_error(params):
    def parse_args(self: ArgumentParser, args=None, namespace=None):
        raise NotImplementedError
    return parse_args


def handle_field_update(params):
    def parse_args(self: ArgumentParser, args=None, namespace=None):
        raise NotImplementedError
    return parse_args


def handle_submit(params):
    def parse_args(self: ArgumentParser, args=None, namespace=None):
        raise NotImplementedError
    return parse_args


def choose_hander(params: GooeyParams, cliargs: List[str]):
    """
    Dispatches to the appropriate handler based on values
    found in the CLI arguments
    """
    with open('tmp.txt', 'w') as f:
        f.write(str(sys.argv))
    if '--gooey-validate-form' in cliargs:
        return validate_form(params)
    elif '--ignore-gooey' in cliargs:
        return bypass_gooey(params)
    else:
        return boostrap_gooey(params)



