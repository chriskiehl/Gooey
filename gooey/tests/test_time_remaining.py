import time
import unittest
from argparse import ArgumentParser
from itertools import *

from tests.harness import instrumentGooey


from gooey.tests import *

class TestFooterTimeRemaining(unittest.TestCase):

    def make_parser(self):
        parser = ArgumentParser(description='description')
        return parser

    def test_time_remaining_visibility(self):
        for testdata in self.testcases():
            with self.subTest(testdata):
                with instrumentGooey(self.make_parser(), timing_options=testdata) as (app, gooeyApp):

                    gooeyApp.showConsole()
                    footer = gooeyApp.footer

                    self.assertEqual(
                        footer.time_remaining_text.Shown,
                        testdata.get('show_time_remaining',False)
                    )

    def test_time_remaining_visibility_on_complete(self):
        for testdata in self.testcases():
            with self.subTest(testdata):
                with instrumentGooey(self.make_parser(), timing_options=testdata) as (app, gooeyApp):

                    gooeyApp.showComplete()
                    footer = gooeyApp.footer


                    if not testdata.get('show_time_remaining') and testdata:
                        self.assertEqual(
                            footer.time_remaining_text.Shown,
                            testdata.get('hide_time_remaining_on_complete',True)
                        )
                    else:
                        return True

    def testcases(self):
        """
        Generate a powerset of all possible combinations of
        the header parameters (empty, some present, all present, all combos)
        """
        iterable = product(['show_time_remaining', 'hide_time_remaining_on_complete'], [True, False])
        allCombinations = list(powerset(iterable))
        return [{k: v for k,v in args}
                for args in allCombinations]


def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))


if __name__ == '__main__':
    unittest.main()