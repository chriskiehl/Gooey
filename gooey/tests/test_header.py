import unittest
from argparse import ArgumentParser
from itertools import *

from tests.harness import instrumentGooey
from gooey.tests import *

class TestGooeyHeader(unittest.TestCase):

    def make_parser(self):
        parser = ArgumentParser(description='description')
        return parser

    def test_header_visibility(self):
        """
        Test that the title and subtitle components correctly show/hide
        based on config settings.

        Verifying Issue #497
        """
        for testdata in self.testcases():
            with self.subTest(testdata):
                with instrumentGooey(self.make_parser(), **testdata) as (app, gooeyApp):
                    header = gooeyApp.header

                    self.assertEqual(
                        header._header.IsShown(),
                        testdata.get('header_show_title', True)
                    )

                    self.assertEqual(
                        header._subheader.IsShown(),
                        testdata.get('header_show_subtitle', True)
                    )


    def test_header_string(self):
        """
        Verify that string in the buildspec get correctly
        placed into the UI.
        """
        parser = ArgumentParser(description='Foobar')
        with instrumentGooey(parser, program_name='BaZzEr') as (app, gooeyApp):
            self.assertEqual(gooeyApp.header._header.GetLabelText(), 'BaZzEr')
            self.assertEqual(gooeyApp.header._subheader.GetLabelText(), 'Foobar')


    def testcases(self):
        """
        Generate a powerset of all possible combinations of
        the header parameters (empty, some present, all present, all combos)
        """
        iterable = product(['header_show_title', 'header_show_subtitle'], [True, False])
        allCombinations = list(powerset(iterable))
        return [{k: v for k,v in args}
                for args in allCombinations]


def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))


if __name__ == '__main__':
    unittest.main()