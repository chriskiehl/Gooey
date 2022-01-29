"""
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!DEBUGGING NOTE!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

PyCharm will inject addition params into stdout when starting
a new process. This can make debugging VERY VERY CONFUSING as
the thing being injected starts complaining about unknown
arguments...

TL;DR: disable the "Attaach to subprocess automatically" option
in the Debugger settings, and the world will be sane again.

See: https://youtrack.jetbrains.com/issue/PY-24929
and: https://www.jetbrains.com/help/pycharm/2017.1/python-debugger.html

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!DEBUGGING NOTE!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
"""
import json
import os
import sys
import traceback
from argparse import ArgumentParser
from copy import deepcopy
from typing import List, Dict

from gooey.python_bindings.dynamics import monkey_patch_for_form_validation
from gooey.python_bindings.dynamics import patch_argument, collect_errors
from gooey.python_bindings.types import GooeyParams
from gooey.python_bindings.coms import serialize_outbound, decode_payload
from gooey.python_bindings.types import PublicGooeyState
from . import cmd_args
from . import config_generator


def noop(*args, **kwargs):
    """
    No-op for dev/null-ing handlers which
    haven't been specified by the user.
    """
    return None


def bypass_gooey(params):
    """
    Bypasses all the Gooey machinery and runs the user's code directly.
    """
    def parse_args(self: ArgumentParser, args=None, namespace=None):
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


def boostrap_gooey(params: GooeyParams):
    """Bootstraps the Gooey UI."""
    def parse_args(self: ArgumentParser, args=None, namespace=None):
        # This import is delayed so it is not in the --ignore-gooey codepath.
        from gooey.gui import bootstrap
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
        bootstrap.run(build_spec)
    return parse_args


def validate_form(params: GooeyParams, write=print, exit=sys.exit):
    """
    Validates the user's current form.
    """
    def merge_errors(state: PublicGooeyState, errors: Dict[str, str]) -> PublicGooeyState:
        changes = deepcopy(state['active_form'])
        for item in changes:
            if item['type'] == 'RadioGroup':
                for subitem in item['options']:  # type: ignore
                    subitem['error'] = errors.get(subitem['id'], None)
                item['error'] = any(x['error'] for x in item['options'])   # type: ignore
            else:
                item['error'] = errors.get(item['id'], None)  # type: ignore

        return PublicGooeyState(active_form=changes)

    def parse_args(self: ArgumentParser, args=None, namespace=None):
        error_registry: Dict[str, Exception] = {}
        patched_parser = monkey_patch_for_form_validation(error_registry, self)
        try:
            args = patched_parser.original_parse_args(args, namespace)  # type: ignore
            state = args.gooey_state
            next_state = merge_errors(state, collect_errors(patched_parser, error_registry, vars(args)))
            write(serialize_outbound(next_state))
            exit(0)
        except Exception as e:
            write(e)
            exit(1)
    return parse_args


def validate_field(params):
    def parse_args(self: ArgumentParser, args=None, namespace=None):
        raise NotImplementedError
    return parse_args


def handle_completed_run(params, write=print, exit=sys.exit):
    def parse_args(self: ArgumentParser, args=None, namespace=None):
        # because we're running under the context of a successful
        # invocation having just completed, the arguments supplied to
        # the parser to trigger it are thus, by definition, safe to parse.
        # So, we don't need any error patching monkey business and just need
        # to attach our specific arg to parse the extra option Gooey passes

        patch_argument(self, '--gooey-state', action='store', type=decode_payload)
        patch_argument(self, '--gooey-run-is-success', default=False, action='store_true')
        patch_argument(self, '--gooey-run-is-failure', default=False, action='store_true')

        try:
            args = self.original_parse_args(args, namespace)  # type: ignore
            form_state = args.gooey_state
            was_success = args.gooey_run_is_success
            # removing the injected gooey value so as not
            # to clutter the user's object
            del args.gooey_state
            del args.gooey_run_is_success
            del args.gooey_run_is_failure
            if was_success:
                next_state = getattr(self, 'on_gooey_success', noop)(args, form_state)  # type: ignore
            else:
                next_state = getattr(self, 'on_gooey_error', noop)(args, form_state)  # type: ignore
            write(serialize_outbound(next_state))
            exit(0)
        except Exception as e:
            write(''.join(traceback.format_stack()))
            write(e)
            exit(1)
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
    elif '--gooey-run-is-success' in cliargs or '--gooey-run-is-failure' in cliargs:
        return handle_completed_run(params)
    elif '--ignore-gooey' in cliargs:
        return bypass_gooey(params)
    else:
        return boostrap_gooey(params)



