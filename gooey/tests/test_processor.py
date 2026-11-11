import os
import re
import subprocess
import sys
import unittest
from unittest.mock import patch

from gooey.gui.processor import ProcessController


class TestProcessor(unittest.TestCase):

    def test_extract_progress(self):
        # should pull out a number based on the supplied
        # regex and expression
        processor = ProcessController(r"^progress: (\d+)%$", None, False, 'utf-8')
        self.assertEqual(processor._extract_progress(b'progress: 50%'), 50)

        processor = ProcessController(r"total: (\d+)%$", None, False, 'utf-8')
        self.assertEqual(processor._extract_progress(b'my cool total: 100%'), 100)

    def test_extract_progress_returns_none_if_no_regex_supplied(self):
        processor = ProcessController(None, None, False, 'utf-8')
        self.assertIsNone(processor._extract_progress(b'Total progress: 100%'))


    def test_extract_progress_returns_none_if_no_match_found(self):
        processor = ProcessController(r'(\d+)%$', None, False, 'utf-8')
        self.assertIsNone(processor._extract_progress(b'No match in dis string'))


    def test_eval_progress(self):
        # given a match in the string, should eval the result
        regex = r'(\d+)/(\d+)$'
        processor = ProcessController(regex, r'x[0] / x[1]', False,False, 'utf-8')
        match = re.search(regex, '50/50')
        self.assertEqual(processor._eval_progress(match), 1.0)
    def test_eval_progress_returns_none_on_failure(self):
        # given a match in the string, should eval the result
        regex = r'(\d+)/(\d+)$'
        processor = ProcessController(regex, r'x[0] *^/* x[1]', False, False,'utf-8')
        match = re.search(regex, '50/50')
        self.assertIsNone(processor._eval_progress(match))

    def test_get_env_force_color(self):
        # Gooey reads the program's output through a pipe, so color libraries
        # such as colored 1.4+ and 2.x add no ANSI codes unless FORCE_COLOR is
        # set. When the rich text console is enabled, Gooey sets FORCE_COLOR
        # for the program so the console has codes to render, unless the user
        # already chose a color setting with FORCE_COLOR or NO_COLOR.
        testcases = [
            # C1: Rich text console is disabled.
            # Expected: FORCE_COLOR is not set.
            (False, {}, None),
            # C2: Rich text console is enabled.
            # Expected: FORCE_COLOR is set to '1'.
            (True, {}, '1'),
            # C3: Rich text console is enabled and the user set FORCE_COLOR.
            # Expected: The user's FORCE_COLOR value is kept.
            (True, {'FORCE_COLOR': '0'}, '0'),
            # C4: Rich text console is enabled and the user set NO_COLOR.
            # Expected: FORCE_COLOR is not set, so NO_COLOR still turns color off.
            (True, {'NO_COLOR': '1'}, None),
        ]
        for input_richtext_controls, input_environment, expected_force_color in testcases:
            with self.subTest(richtext_controls=input_richtext_controls, environment=input_environment):
                with patch.dict(os.environ, input_environment):
                    for name in {'FORCE_COLOR', 'NO_COLOR'} - set(input_environment):
                        os.environ.pop(name, None)
                    processor = ProcessController(None, None, False, 'utf-8', richtext_controls=input_richtext_controls)
                    actual_force_color = processor._get_env().get('FORCE_COLOR')
                self.assertEqual(actual_force_color, expected_force_color)

    def test_get_env_lets_colored_output_reach_the_console(self):
        # A program run with the rich text console enabled prints text styled
        # with colored to a pipe, as it does under Gooey.
        # Expected: The ANSI codes reach Gooey with no FORCE_COLOR set by the user.
        input_program = 'import colored; print(colored.stylize("hello", colored.fg("green")))'
        with patch.dict(os.environ):
            os.environ.pop('FORCE_COLOR', None)
            os.environ.pop('NO_COLOR', None)
            processor = ProcessController(None, None, False, 'utf-8', richtext_controls=True)
            program_output = subprocess.run(
                [sys.executable, '-c', input_program],
                env=processor._get_env(), stdout=subprocess.PIPE, check=True,
            )
        actual_program_output = program_output.stdout.decode().strip()
        self.assertEqual(actual_program_output, '\x1b[38;5;2mhello\x1b[0m')
