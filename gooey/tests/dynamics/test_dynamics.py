import unittest
from argparse import ArgumentParser
from typing import Dict
from unittest.mock import MagicMock

from python_bindings.dynamics import patch_argument, check_value


class TestDynamicUpdates(unittest.TestCase):

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


    def test_check_value_wrapper(self):
        parser = ArgumentParser()
        parser.add_argument('foo', choices=[1, 2, 3])
        parser.add_argument('bar', choices=[1, 2, 3])

        # demo'ing default behavior. Prior to the patching, argparse
        # explodes during the check_value call if any invariants are violated
        def kaboom():
            raise Exception('boom')
        mock = MagicMock(side_effect=kaboom)
        try:
            parser.error = mock
            parser.parse_args(['nope', 'not-a-valid-choice'])
            self.fail('Should have thrown an error during check_value')
        except Exception as e:
            # note that we exploded after the first one
            # thus the error method was only called once
            assert mock.called
            assert mock.call_count == 1

        # What we want is to capture ALL errors without failing early
        arbitrary_dict: Dict[str, Exception] = {}
        self.assertTrue(len(arbitrary_dict) == 0)


        # So we patch the check_value method witho our own
        original_fn = ArgumentParser._check_value
        ArgumentParser._check_value = check_value(arbitrary_dict, original_fn)
        parser.parse_args(['nope', 'not-a-valid-choice'])

        # now, rather than failing after the very first violation, all
        # errors are recorded into our map
        self.assertTrue(len(arbitrary_dict) > 0)
        assert 'foo' in arbitrary_dict
        assert 'bar' in arbitrary_dict

        assert 'invalid choice' in str(arbitrary_dict['foo'])
        assert 'invalid choice' in str(arbitrary_dict['bar'])





