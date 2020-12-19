import unittest
from unittest.mock import patch

from tests.harness import instrumentGooey
from gooey import GooeyParser
from gooey.tests import *

class TestGooeySlider(unittest.TestCase):

    def makeParser(self, **kwargs):
        parser = GooeyParser(description='description')
        parser.add_argument('--slider', widget="Slider", **kwargs)
        return parser


    def testSliderDefault(self):
        cases = [
            [{}, 0],
            [{'default': 0}, 0],
            [{'default': 10}, 10],
            [{'default': 76}, 76],
            # note that WX caps the value
            # unless explicitly widened via gooey_options
            [{'default': 81234}, 100],
            # here we set the max to something higher than
            # the default and all works as expected.
            # this is a TODO for validation
            [{'default': 81234, 'gooey_options': {'max': 99999}}, 81234],

            # Initial Value cases
            [{}, 0],
            [{'gooey_options': {'initial_value': 0}}, 0],
            [{'gooey_options': {'initial_value': 10}}, 10],
            [{'gooey_options': {'initial_value': 76}}, 76],
            # note that WX caps the value
            # unless explicitly widened via gooey_options
            [{'gooey_options': {'initial_value': 81234}}, 100],
            # here we set the max to something higher than
            # the default and all works as expected.
            # this is a TODO for validation
            [{'gooey_options': {'initial_value': 81234, 'max': 99999}}, 81234],
        ]
        for inputs, expected in cases:
            with self.subTest(inputs):
                parser = self.makeParser(**inputs)
                with instrumentGooey(parser) as (app, gooeyApp):
                    slider = gooeyApp.configs[0].reifiedWidgets[0]
                    self.assertEqual(slider.getValue()['rawValue'], expected)

    def testZerosAreReturned(self):
        """
        Originally the formatter was dropping '0' due to
        it being interpreted as falsey
        """
        parser = self.makeParser()
        with instrumentGooey(parser) as (app, gooeyApp):
            field = gooeyApp.configs[0].reifiedWidgets[0]
            result = field.getValue()
            self.assertEqual(result['rawValue'], 0)
            self.assertIsNotNone(result['cmd'])


if __name__ == '__main__':
    unittest.main()