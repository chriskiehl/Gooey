import unittest
from gooey.gui import cli


class TestCliStringCreation(unittest.TestCase):

    # TODO: exercise the formValidationCase (which will require tedious test data creation)
    def test_cli(self):
        print(cli.buildCliString('target', 'cmd', ['pos1', 'pos2'], ['-a 1', '-b 2']))

        positionals = [
            {'clitype': 'positional', 'cmd': 'pos1', 'required': True},
            {'clitype': 'positional', 'cmd': 'pos2', 'required': True}
        ]

        optionals = [
            {'clitype': 'optional', 'cmd': '-a 1', 'required': False},
            {'clitype': 'optional', 'cmd': '-b 2', 'required': False},
        ]

        # print(cli.formValidationCmd('target', 'cmd', positionals, optionals))