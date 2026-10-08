import unittest
from argparse import ArgumentParser

from tests.harness import instrumentGooey
from gooey.tests import *


class TestFooterTimeRemaining(unittest.TestCase):

    def make_parser(self):
        parser = ArgumentParser(description='description')
        return parser

    def test_time_remaining_visibility(self):
        # Visibility of the time remaining text while the program is running.
        # Only show_time_remaining affects it; hide_time_remaining_on_complete does not.
        testcases = [
            # C1: No timing options are given.
            # Expected: Text is hidden, since show_time_remaining defaults to False.
            ({}, False),
            # C2: show_time_remaining is True.
            # Expected: Text is shown.
            ({'show_time_remaining': True}, True),
            # C3: show_time_remaining is False.
            # Expected: Text is hidden.
            ({'show_time_remaining': False}, False),
            # C4: show_time_remaining is True and hide_time_remaining_on_complete is True.
            # Expected: Text is shown and hide_time_remaining_on_complete does not
            # affect the visibility while running, since it only applies after completion.
            ({'show_time_remaining': True, 'hide_time_remaining_on_complete': True}, True),
            # C5: show_time_remaining is False and hide_time_remaining_on_complete is False.
            # Expected: Text is hidden and hide_time_remaining_on_complete does not
            # affect the visibility while running, since it only applies after completion.
            ({'show_time_remaining': False, 'hide_time_remaining_on_complete': False}, False),
        ]
        for input_timing_options, expected_is_text_shown in testcases:
            with self.subTest(input_timing_options):
                with instrumentGooey(self.make_parser(), timing_options=input_timing_options) as (app, gooeyApp):
                    gooeyApp.showConsole()
                    actual_is_text_shown = gooeyApp.footer.time_remaining_text.IsShown()
                    self.assertEqual(actual_is_text_shown, expected_is_text_shown)

    def test_time_remaining_visibility_on_complete(self):
        # Visibility of the time remaining text once the program completes.
        # Only hide_time_remaining_on_complete affects it; show_time_remaining does not.
        testcases = [
            # C1: No timing options are given.
            # Expected: Text is hidden, since hide_time_remaining_on_complete defaults to True.
            ({}, False),
            # C2: hide_time_remaining_on_complete is True.
            # Expected: Text is hidden.
            ({'hide_time_remaining_on_complete': True}, False),
            # C3: hide_time_remaining_on_complete is False.
            # Expected: Text is shown.
            ({'hide_time_remaining_on_complete': False}, True),
            # C4: show_time_remaining is True and hide_time_remaining_on_complete is True.
            # Expected: Text is hidden and show_time_remaining does not
            # affect the visibility once the program has finished,
            # since it only applies while running.
            ({'show_time_remaining': True, 'hide_time_remaining_on_complete': True}, False),
            # C5: show_time_remaining is True and hide_time_remaining_on_complete is False.
            # Expected: Text is shown and show_time_remaining does not
            # affect the visibility once the program has finished,
            # since it only applies while running.
            ({'show_time_remaining': True, 'hide_time_remaining_on_complete': False}, True),
        ]
        for input_timing_options, expected_is_text_shown in testcases:
            with self.subTest(input_timing_options):
                with instrumentGooey(self.make_parser(), timing_options=input_timing_options) as (app, gooeyApp):
                    gooeyApp.showComplete()
                    actual_is_text_shown = gooeyApp.footer.time_remaining_text.IsShown()
                    self.assertEqual(actual_is_text_shown, expected_is_text_shown)


if __name__ == '__main__':
    unittest.main()
