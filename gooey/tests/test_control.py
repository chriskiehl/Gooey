import json
import unittest
from argparse import ArgumentParser
from contextlib import contextmanager
from pprint import pprint
from typing import Dict, List
from unittest.mock import MagicMock, patch

import sys
import shlex

from wx._core import CommandEvent

from gooey import GooeyParser
from python_bindings.coms import decode_payload, deserialize_inbound
from python_bindings.dynamics import patch_argument, check_value
from gooey.python_bindings import control
from gooey.python_bindings.parameters import gooey_params
from gooey.gui import state as s
from gooey.python_bindings.schema import validate_public_state
from python_bindings.types import FormField

from tests.harness import instrumentGooey

from gooey.tests import *


def custom_type(x):
    if x == '1234':
        return x
    else:
        raise Exception('KABOOM!')


class TestControl(unittest.TestCase):

    def tearDown(self):
        """
        Undoes the monkey patching after every tests
        """
        if hasattr(ArgumentParser, 'original_parse_args'):
            ArgumentParser.parse_args = ArgumentParser.original_parse_args

    def test_validate_form(self):
        """
        Testing the major validation cases we support.
        """
        writer = MagicMock()
        exit = MagicMock()
        monkey_patch = control.validate_form(gooey_params(), write=writer, exit=exit)
        ArgumentParser.original_parse_args = ArgumentParser.parse_args
        ArgumentParser.parse_args = monkey_patch

        parser = GooeyParser()
        # examples:
        # ERROR: mismatched builtin type
        parser.add_argument('a', type=int, gooey_options={'initial_value': 'not-an-int'})
        # ERROR: mismatched custom type
        parser.add_argument('b', type=custom_type, gooey_options={'initial_value': 'not-a-float'})
        # ERROR: missing required positional arg
        parser.add_argument('c')
        # ERROR: missing required 'optional' arg
        parser.add_argument('--oc', required=True)
        # VALID: This is one of the bizarre cases which are possible
        # but don't make much sense. It should pass through as valid
        # because there's no way for us to send a 'not present optional value'
        parser.add_argument('--bo', action='store_true', required=True)
        # ERROR: a required mutex group, with no args supplied.
        # Should flag all as missing.
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument('--gp1-a', type=str)
        group.add_argument('--gp1-b', type=str)

        # ERROR: required mutex group with a default option but nothing
        # selected will still fail
        group2 = parser.add_mutually_exclusive_group(required=True)
        group2.add_argument('--gp2-a', type=str)
        group2.add_argument('--gp2-b', type=str, default='Heeeeyyyyy')

        # VALID: now, same as above, but now the option is actually enabled via
        # the initial selection. No error.
        group3 = parser.add_mutually_exclusive_group(required=True, gooey_options={'initial_selection': 1})
        group3.add_argument('--gp3-a', type=str)
        group3.add_argument('--gp3-b', type=str, default='Heeeeyyyyy')
        # VALID: optional mutex.
        group4 = parser.add_mutually_exclusive_group()
        group4.add_argument('--gp4-a', type=str)
        group4.add_argument('--gp4-b', type=str)
        # VALID: arg present and type satisfied
        parser.add_argument('ga', type=str, gooey_options={'initial_value': 'whatever'})
        # VALID: arg present and custom type satisfied
        parser.add_argument('gb', type=custom_type, gooey_options={'initial_value': '1234'})
        # VALID: optional
        parser.add_argument('--gc')

        # now we're adding the same
        with instrumentGooey(parser, target='test') as (app, frame, gapp):
            # we start off with no errors
            self.assertFalse(s.has_errors(gapp.fullState()))

            # now we feed our form-validation
            cmd = s.buildFormValidationCmd(gapp.fullState())
            asdf = shlex.split(cmd)[1:]
            parser.parse_args(shlex.split(cmd)[1:])
            assert writer.called
            assert exit.called


        result = deserialize_inbound(writer.call_args[0][0].encode('utf-8'), 'utf-8')
        # Host->Gooey communication is all done over the PublicGooeyState schema
        # as such, we coarsely validate it's shape here
        validate_public_state(result)

        # manually merging the two states back together
        nextState = s.mergeExternalState(gapp.fullState(), result)
        # and now we find that we have errors!
        self.assertTrue(s.has_errors(nextState))
        items = s.activeFormState(nextState)
        self.assertIn('invalid literal', get_by_id(items, 'a')['error'])
        self.assertIn('KABOOM!', get_by_id(items, 'b')['error'])
        self.assertIn('required', get_by_id(items, 'c')['error'])
        self.assertIn('required', get_by_id(items, 'oc')['error'])
        for item in get_by_id(items, 'group_gp1_a_gp1_b')['options']:
            self.assertIsNotNone(item['error'])
        for item in get_by_id(items, 'group_gp2_a_gp2_b')['options']:
            self.assertIsNotNone(item['error'])

        for item in get_by_id(items, 'group_gp3_a_gp3_b')['options']:
            self.assertIsNone(item['error'])
        # should be None, since this one was entirely optional
        for item in get_by_id(items, 'group_gp4_a_gp4_b')['options']:
            self.assertIsNone(item['error'])
        self.assertIsNone(get_by_id(items, 'bo')['error'])
        self.assertIsNone(get_by_id(items, 'ga')['error'])
        self.assertIsNone(get_by_id(items, 'gb')['error'])
        self.assertIsNone(get_by_id(items, 'gc')['error'])


    def test_subparsers(self):
        """
        Making sure that subparsers are handled correctly and
        all validations still work as expected.
        """
        writer = MagicMock()
        exit = MagicMock()
        monkey_patch = control.validate_form(gooey_params(), write=writer, exit=exit)
        ArgumentParser.original_parse_args = ArgumentParser.parse_args
        ArgumentParser.parse_args = monkey_patch

        def build_parser():
            # we build a new parser for each subtest
            # since we monkey patch the hell out of it
            # each time
            parser = GooeyParser()
            subs = parser.add_subparsers()
            foo = subs.add_parser('foo')
            foo.add_argument('a')
            foo.add_argument('b')
            foo.add_argument('p')

            bar = subs.add_parser('bar')
            bar.add_argument('a')
            bar.add_argument('b')
            bar.add_argument('z')
            return parser

        parser = build_parser()
        with instrumentGooey(parser, target='test') as (app, frame, gapp):
            with self.subTest('first subparser'):
                # we start off with no errors
                self.assertFalse(s.has_errors(gapp.fullState()))

                cmd = s.buildFormValidationCmd(gapp.fullState())
                parser.parse_args(shlex.split(cmd)[1:])
                assert writer.called
                assert exit.called

                result = deserialize_inbound(writer.call_args[0][0].encode('utf-8'), 'utf-8')
                nextState = s.mergeExternalState(gapp.fullState(), result)
                # by default, the subparser defined first, 'foo', is selected.
                self.assertIn('foo', nextState['forms'])
                # and we should find its attributes
                expected = {'a', 'b', 'p'}
                actual = {x['id'] for x in nextState['forms']['foo']}
                self.assertEqual(expected, actual)


        parser = build_parser()
        with instrumentGooey(parser, target='test') as (app, frame, gapp):
            with self.subTest('Second subparser'):
                # mocking a 'selection change' event to select
                # the second subparser
                event = MagicMock()
                event.Selection = 1
                gapp.handleSelectAction(event)

                # Flushing our events by running the main loop
                wx.CallLater(1, app.ExitMainLoop)
                app.MainLoop()

                cmd = s.buildFormValidationCmd(gapp.fullState())
                parser.parse_args(shlex.split(cmd)[1:])
                assert writer.called
                assert exit.called

                result = deserialize_inbound(writer.call_args[0][0].encode('utf-8'), 'utf-8')
                nextState = s.mergeExternalState(gapp.fullState(), result)
                # Now our second subparer, 'bar', should be present.
                self.assertIn('bar', nextState['forms'])
                # and we should find its attributes
                expected = {'a', 'b', 'z'}
                actual = {x['id'] for x in nextState['forms']['bar']}
                self.assertEqual(expected, actual)


    def test_ignore_gooey(self):
        parser = GooeyParser()
        subs = parser.add_subparsers()
        foo = subs.add_parser('foo')
        foo.add_argument('a')
        foo.add_argument('b')
        foo.add_argument('p')

        bar = subs.add_parser('bar')
        bar.add_argument('a')
        bar.add_argument('b')
        bar.add_argument('z')

        control.bypass_gooey(gooey_params())(parser)

def get_by_id(items: List[FormField], id: str):
    return [x for x in items if x['id'] == id][0]



