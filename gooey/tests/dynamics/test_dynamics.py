import unittest
from argparse import ArgumentParser
from typing import Dict
from unittest.mock import MagicMock

from python_bindings.dynamics import patch_argument, monkey_patch_for_form_validation


class TestDynamicUpdates(unittest.TestCase):

    def tearDown(self):
        """
        Undoes the monkey patching after every tests
        """
        if hasattr(ArgumentParser, 'original_parse_args'):
            ArgumentParser.parse_args = ArgumentParser.original_parse_args

    def test_patch_argument(self):
        """
        Asserting that regardless of parser complexity, we attach our
        new argument at every level.
        """
        parser = ArgumentParser()
        subparsers = parser.add_subparsers()
        # multiple subparsers
        a = subparsers.add_parser('a')
        b = subparsers.add_parser('b')

        a.add_argument('--level-1')
        b.add_argument('--level-1')

        # deeply nested subparsers
        a_subparsers = a.add_subparsers()
        b_subparsers = b.add_subparsers()

        # nested args:
        a__nested = a_subparsers.add_parser('a1')
        b__nested = b_subparsers.add_parser('b1')

        a__nested.add_argument('--level-2')
        b__nested.add_argument('--level-2')

        # sanity check / showing the parser behavior
        # we've got two levels of parser nesting, each level
        # has some options available.
        mock = MagicMock()
        ArgumentParser.error = mock
        assert parser.parse_args('a --level-1 some-value'.split())
        assert parser.parse_args('b --level-1 some-value'.split())
        assert parser.parse_args('a a1 --level-2 some-value'.split())
        assert parser.parse_args('b b1 --level-2 some-value'.split())
        assert not mock.called

        # if we try passing an arbitrary unknown flag we explode
        # patching over the `error` method which usually sys.exit's
        # for any errors.
        parser.parse_args('a --level-1 some-value --some-flag'.split())
        assert mock.called

        patch_argument(parser, '--some-flag', action='store_true')
        mock.reset_mock()
        # now ever call combination accepts the flag we added
        assert parser.parse_args('--some-flag'.split())
        assert parser.parse_args('a --level-1 some-value --some-flag'.split())
        assert parser.parse_args('b --level-1 some-value --some-flag'.split())
        assert parser.parse_args('a a1 --level-2 some-value --some-flag'.split())
        assert parser.parse_args('b b1 --level-2 some-value --some-flag'.split())
        assert not mock.called

