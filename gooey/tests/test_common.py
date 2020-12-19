import unittest
from collections import namedtuple

from tests.harness import instrumentGooey
from gooey import GooeyParser
from gooey.tests import *

Case = namedtuple('Case', 'inputs initialExpected')


class TestCommonProperties(unittest.TestCase):
    """
    Test options and functionality
    common across all widgets.
    """

    def makeParser(self, **kwargs):
        parser = GooeyParser(description='description')
        parser.add_argument('--widget', **kwargs)
        return parser

    def testInitialValue(self):
        widgets = ['ColourChooser',
                   'CommandField',
                   'DateChooser', 'DirChooser', 'FileChooser', 'FileSaver',
                   'FilterableDropdown',  'MultiDirChooser', 'MultiFileChooser',
                   'PasswordField',  'TextField', 'Textarea', 'TimeChooser']

        cases = [
            # initial_value supersedes, default
            Case(
                {'default': 'default', 'gooey_options': {'initial_value': 'some val'}},
                'some val'),
            Case(
                {'gooey_options': {'initial_value': 'some val'}},
                 'some val'),
            Case(
                {'default': 'default', 'gooey_options': {}},
                 'default'),
            Case({'default': 'default'},
                 'default')
        ]

        for widgetName in widgets:
            with self.subTest(widgetName):
                for case in cases:
                    parser = self.makeParser(widget=widgetName, **case.inputs)
                    with instrumentGooey(parser) as (app, gooeyApp):
                        widget = gooeyApp.configs[0].reifiedWidgets[0]
                        self.assertEqual(widget.getValue()['rawValue'], case.initialExpected)


if __name__ == '__main__':
    unittest.main()
