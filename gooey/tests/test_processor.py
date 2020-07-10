import re
import unittest

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
