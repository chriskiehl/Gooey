import unittest

from tests.harness import instrumentGooey
from gooey import GooeyParser
from gooey.tests import *



class TestCheckbox(unittest.TestCase):

    def makeParser(self, **kwargs):
        parser = GooeyParser(description='description')
        parser.add_argument(
            '--widget',
            action='store_true',
            **kwargs)
        return parser


    def testInitialValue(self):
        cases = [
            # `initial` should supersede `default`
            {'inputs': {'default': False,
                        'widget': 'CheckBox',
                        'gooey_options': {'initial_value': True}},
             'expect': True},

            {'inputs': {'gooey_options': {'initial_value': True},
                        'widget': 'CheckBox'},
             'expect': True},

            {'inputs': {'gooey_options': {'initial_value': False},
                        'widget': 'CheckBox'},
             'expect': False},

            {'inputs': {'default': True,
                        'widget': 'CheckBox',
                        'gooey_options': {}},
             'expect': True},

            {'inputs': {'default': True,
                        'widget': 'CheckBox'},
             'expect': True},

            {'inputs': {'widget': 'CheckBox'},
             'expect': False}
        ]
        for case in cases:
            with self.subTest(case):
                parser = self.makeParser(**case['inputs'])
                with instrumentGooey(parser) as (app, gooeyApp):
                    widget = gooeyApp.configs[0].reifiedWidgets[0]
                    self.assertEqual(widget.getValue()['rawValue'], case['expect'])



if __name__ == '__main__':
    unittest.main()