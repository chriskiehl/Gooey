import unittest
from collections import namedtuple

from tests.harness import instrumentGooey
from gooey import GooeyParser
from gooey.tests import *

Case = namedtuple('Case', 'inputs initialExpected expectedAfterClearing')

class TestTextField(unittest.TestCase):

    def makeParser(self, **kwargs):
        parser = GooeyParser(description='description')
        parser.add_argument('--widget', widget="TextField", **kwargs)
        return parser


    def testPlaceholder(self):
        cases = [
            [{}, ''],
            [{'placeholder': 'Hello'}, 'Hello']
        ]
        for options, expected in cases:
            parser = self.makeParser(gooey_options=options)
            with instrumentGooey(parser) as (app, gooeyApp):
                # because of how poorly designed the Gooey widgets are
                # we have to reach down 3 levels in order to find the
                # actual WX object we need to test.
                widget = gooeyApp.configs[0].reifiedWidgets[0].widget
                self.assertEqual(widget.widget.GetHint(), expected)




    def testDefaultAndInitialValue(self):
        cases = [
            # initial_value takes precedence when both are present
            Case(
                {'default': 'default_val', 'gooey_options': {'initial_value': 'some val'}},
                'some val',
                None),
            # when no default is present
            # Case({'gooey_options': {'initial_value': 'some val'}},
            #  'some val',
            #  ''),
            # [{'default': 'default', 'gooey_options': {}},
            #  'default'],
            # [{'default': 'default'},
            #  'default'],
        ]
        for case in cases:
            parser = self.makeParser(**case.inputs)
            with instrumentGooey(parser) as (app, gooeyApp):
                widget = gooeyApp.configs[0].reifiedWidgets[0]
                self.assertEqual(widget.getValue()['rawValue'], case.initialExpected)
                widget.setValue('')
                print(widget.getValue())
                self.assertEqual(widget.getValue()['cmd'], case.expectedAfterClearing)

if __name__ == '__main__':
    unittest.main()