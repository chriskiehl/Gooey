import unittest
from random import randint
from unittest.mock import patch

from tests.harness import instrumentGooey
from gooey import GooeyParser
from gooey.tests import *

class TestNumbericInputs(unittest.TestCase):

    def makeParser(self, **kwargs):
        parser = GooeyParser(description='description')
        parser.add_argument('--input', **kwargs)
        return parser


    def testDefault(self):
        cases = [
            [{'widget': 'IntegerField'}, 0],
            [{'default': 0, 'widget': 'IntegerField'}, 0],
            [{'default': 10, 'widget': 'IntegerField'}, 10],
            [{'default': 76, 'widget': 'IntegerField'}, 76],
            # note that WX caps the value
            # unless explicitly widened via gooey_options
            [{'default': 81234, 'widget': 'IntegerField'}, 100],
            # here we set the max to something higher than
            # the default and all works as expected.
            # this is a TODO for validation
            [{'default': 81234, 'widget': 'IntegerField', 'gooey_options': {'max': 99999}}, 81234],
            # Initial Value cases
            [{'widget': 'IntegerField', 'gooey_options': {'initial_value': 0}}, 0],
            [{'widget': 'IntegerField', 'gooey_options': {'initial_value': 10}}, 10],
            [{'widget': 'IntegerField', 'gooey_options': {'initial_value': 76}}, 76],
            # note that WX caps the value
            # unless explicitly widened via gooey_options
            [{'widget': 'IntegerField', 'gooey_options': {'initial_value': 81234}}, 100],
            # here we set the max to something higher than
            # the default and all works as expected.
            # this is a TODO for validation
            [{'widget': 'IntegerField', 'gooey_options': {'initial_value': 81234, 'max': 99999}}, 81234],

            [{'widget': 'DecimalField'}, 0],
            [{'default': 0, 'widget': 'DecimalField'}, 0],
            [{'default': 81234, 'widget': 'DecimalField'}, 100],
            [{'default': 81234, 'widget': 'DecimalField', 'gooey_options': {'max': 99999}}, 81234],
            # Initial Value cases
            [{'widget': 'DecimalField', 'gooey_options': {'initial_value': 0}}, 0],
            [{'widget': 'DecimalField', 'gooey_options': {'initial_value': 10}}, 10],
            [{'widget': 'DecimalField', 'gooey_options': {'initial_value': 76}}, 76],
            # note that WX caps the value
            # unless explicitly widened via gooey_options
            [{'widget': 'DecimalField', 'gooey_options': {'initial_value': 81234}}, 100],
            # here we set the max to something higher than
            # the default and all works as expected.
            # this is a TODO for validation
            [{'widget': 'DecimalField', 'gooey_options': {'initial_value': 81234, 'max': 99999}}, 81234],
        ]
        for inputs, expected in cases:
            with self.subTest(inputs):
                parser = self.makeParser(**inputs)
                with instrumentGooey(parser) as (app, gooeyApp):
                    input = gooeyApp.configs[0].reifiedWidgets[0]
                    self.assertEqual(input.getValue()['rawValue'], expected)

    def testGooeyOptions(self):
        cases = [
            {'widget': 'DecimalField', 'gooey_options': {'min': -100, 'max': 1234, 'increment': 1.240}},
            {'widget': 'DecimalField', 'gooey_options': {'min': 1234, 'max': 3456, 'increment': 2.2}},
            {'widget': 'IntegerField', 'gooey_options': {'min': -100, 'max': 1234}},
            {'widget': 'IntegerField', 'gooey_options': {'min': 1234, 'max': 3456}}
        ];
        using = {
            'min': lambda widget: widget.GetMin(),
            'max': lambda widget: widget.GetMax(),
            'increment': lambda widget: widget.GetIncrement(),

        }
        for case in cases:
            with self.subTest(case):
                parser = self.makeParser(**case)
                with instrumentGooey(parser) as (app, gooeyApp):
                    wxWidget = gooeyApp.configs[0].reifiedWidgets[0].widget
                    for option, value in case['gooey_options'].items():
                        self.assertEqual(using[option](wxWidget), value)


    def testZerosAreReturned(self):
        """
        Originally the formatter was dropping '0' due to
        it being interpreted as falsey
        """
        parser = self.makeParser(widget='IntegerField')
        with instrumentGooey(parser) as (app, gooeyApp):
            field = gooeyApp.configs[0].reifiedWidgets[0]
            result = field.getValue()
            self.assertEqual(result['rawValue'], 0)
            self.assertIsNotNone(result['cmd'])

    def testNoLossOfPrecision(self):
        parser = self.makeParser(widget='DecimalField', default=12.23534, gooey_options={'precision': 20})
        with instrumentGooey(parser) as (app, gooeyApp):
            field = gooeyApp.configs[0].reifiedWidgets[0]
            result = field.getValue()
            self.assertEqual(result['rawValue'], 12.23534)
            self.assertIsNotNone(result['cmd'])




if __name__ == '__main__':
    unittest.main()