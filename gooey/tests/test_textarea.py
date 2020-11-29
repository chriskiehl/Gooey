import unittest

from tests.harness import instrumentGooey
from gooey import GooeyParser
from gooey.tests import *

class TestTextarea(unittest.TestCase):

    def makeParser(self, **kwargs):
        parser = GooeyParser(description='description')
        parser.add_argument('--widget', widget="Textarea", **kwargs)
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
                widget = gooeyApp.configs[0].reifiedWidgets[0]
                self.assertEqual(widget.widget.GetHint(), expected)



if __name__ == '__main__':
    unittest.main()