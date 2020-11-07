import unittest

from gooey import GooeyParser
from gooey.python_bindings import cmd_args
from argparse import ArgumentParser
from gooey.tests import *


class TextCommandLine(unittest.TestCase):

    def test_default_overwritten(self):
        parser = GooeyParser()
        ArgumentParser.original_parse_args = ArgumentParser.parse_args

        parser.add_argument('arg', type=int, default=0)

        # Supply 1 as command line argument, check that it overwrites argparse default
        cmd_args.parse_cmd_args(parser, ['1'])
        argdefault = next(action for action in parser._actions if action.dest == 'arg').default
        self.assertEqual(argdefault, 1)

    def test_required_not_enforced(self):
        parser = GooeyParser()
        ArgumentParser.original_parse_args = ArgumentParser.parse_args

        parser.add_argument('--arg', type=int, required=True)
        parser.add_argument('--argn', type=int, nargs='+')
        parser.add_argument('argp', type=int)
        mutex=parser.add_mutually_exclusive_group(required=True)
        mutex.add_argument('--one', action='store_true')
        mutex.add_argument('--two', action='store_true')

        # No error when we don't provide required arguments
        cmd_args.parse_cmd_args(parser)

        # Test that required/argn have been restored in parser
        argrequired = next(action for action in parser._actions if action.dest == 'arg').required
        self.assertEqual(argrequired, True)
        argnnargs = next(action for action in parser._actions if action.dest == 'argn').nargs
        self.assertEqual(argnnargs, '+')
        argpnargs = next(action for action in parser._actions if action.dest == 'argp').nargs
        self.assertEqual(argpnargs, None)
        mutexrequired = next(mutex for mutex in parser._mutually_exclusive_groups).required
        self.assertEqual(mutexrequired, True)

    def test_cmd_args_subparser(self):
        parser = GooeyParser()
        subparsers = parser.add_subparsers(dest='subparser')
        subparserA = subparsers.add_parser('A')
        subparserB = subparsers.add_parser('B')
        subparserA.add_argument('argA', type=int, default=0)
        subparserB.add_argument('argB', type=int, default=0)

        ArgumentParser.original_parse_args = ArgumentParser.parse_args

        cmd_args.parse_cmd_args(parser, ['A', '1'])

        # Check that argA is overwritten but not argB
        subparseraction = next(action for action in parser._actions if action.dest == 'subparser')
        argAdefault = next(action for action in subparseraction.choices['A']._actions if action.dest == 'argA').default
        self.assertEqual(argAdefault, 1)
        argBdefault = next(action for action in subparseraction.choices['B']._actions if action.dest == 'argB').default
        self.assertEqual(argBdefault, 0)
