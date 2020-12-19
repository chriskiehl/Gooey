import unittest

from tests.harness import instrumentGooey
from gooey import GooeyParser
from gooey.tests import *



class TestListbox(unittest.TestCase):

    def makeParser(self, **kwargs):
        parser = GooeyParser(description='description')
        parser.add_argument(
            '--widget',
            widget="Listbox",
            nargs="*",
            **kwargs)
        return parser

    def testInitialValue(self):
        cases = [
            # `initial` should supersede `default`
            {'inputs': {'default': 'b',
                        'choices': ['a', 'b', 'c'],
                        'gooey_options': {'initial_value': 'a'}},
             'expect': ['a']},

            {'inputs': {'choices': ['a', 'b', 'c'],
                        'gooey_options': {'initial_value': 'a'}},
             'expect': ['a']},

            {'inputs': {'choices': ['a', 'b', 'c'],
                        'gooey_options': {'initial_value': ['a', 'c']}},
             'expect': ['a', 'c']},

            {'inputs': {'choices': ['a', 'b', 'c'],
                        'default': 'b',
                        'gooey_options': {}},
             'expect': ['b']},

            {'inputs': {'choices': ['a', 'b', 'c'],
                        'default': 'b'},
             'expect': ['b']},

            {'inputs': {'choices': ['a', 'b', 'c']},
             'expect': []}
        ]
        for case in cases:
            with self.subTest(case):
                parser = self.makeParser(**case['inputs'])
                with instrumentGooey(parser) as (app, gooeyApp):
                    widget = gooeyApp.configs[0].reifiedWidgets[0]
                    self.assertEqual(widget.getValue()['rawValue'], case['expect'])



if __name__ == '__main__':
    unittest.main()