import unittest

from tests.harness import instrumentGooey
from gooey import GooeyParser
from gooey.tests import *



class TestCounter(unittest.TestCase):

    def makeParser(self, **kwargs):
        parser = GooeyParser(description='description')
        parser.add_argument(
            '--widget',
            action='count',
            widget="Counter",
            **kwargs)
        return parser


    def testInitialValue(self):
        cases = [
            # `initial` should supersede `default`
            {'inputs': {'default': 1,
                        'gooey_options': {'initial_value': 3}},
             'expect': '3'},

            {'inputs': {'gooey_options': {'initial_value': 1}},
             'expect': '1'},

            {'inputs': {'default': 2,
                        'gooey_options': {}},
             'expect': '2'},

            {'inputs': {'default': 1},
             'expect': '1'},

            {'inputs': {},
             'expect': None}
        ]
        for case in cases:
            with self.subTest(case):
                parser = self.makeParser(**case['inputs'])
                with instrumentGooey(parser) as (app, gooeyApp):
                    widget = gooeyApp.configs[0].reifiedWidgets[0]
                    self.assertEqual(widget.getValue()['rawValue'], case['expect'])



if __name__ == '__main__':
    unittest.main()