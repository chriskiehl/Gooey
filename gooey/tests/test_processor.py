import re
import unittest

from gooey.gui.processor import ProcessController


class TestProcessor(unittest.TestCase):

    def test_extract_progress(self):
        # should pull out a number based on the supplied
        # regex and expression
        processor = ProcessController("^progress: (\d+)%$", None, False, 'utf-8')
        self.assertEqual(processor._extract_progress(b'progress: 50%'), 50)

        processor = ProcessController("total: (\d+)%$", None, False, 'utf-8')
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
        processor = ProcessController(regex, r'x[0] / x[1]', False, 'utf-8')
        match = re.search(regex, '50/50')
        self.assertEqual(processor._eval_progress(match), 1.0)


    def test_time_elapsed(self):
        # Check that time elapsed is greater than zero
        processor = ProcessController("^progress: (\d+)%$", None, False, 'utf-8')
        _start_time = processor._get_current_time()
        elapsed, _ = processor._calculate_time_remaining(processor._extract_progress(b'progress: 30%'),_start_time)
        self.assertGreater(elapsed,0)

    def test_time_remaining(self):
        # Check that time elapsed is greater than zero
        processor = ProcessController("^progress: (\d+)%$", None, False, 'utf-8')
        _start_time = processor._get_current_time()
        _, remaining = processor._calculate_time_remaining(processor._extract_progress(b'progress: 30%'),_start_time)
        self.assertGreater(remaining,0)

    def test_current_time(self):
        # Test that current time is greater than zero
        processor = ProcessController("^progress: (\d+)%$", None, False, 'utf-8')
        self.assertGreater(processor._get_current_time(),0)

    
    def test_format_interval(self):
        # Test same as TQDM https://github.com/tqdm/tqdm/blob/0cd9448b2bc08125e74538a2aea6af42ee1a7b6f/tqdm/tests/tests_tqdm.py#L234
        # but in unittest form
        format_interval = processor = ProcessController("^progress: (\d+)%$", None, False, 'utf-8').format_interval

        self.assertEqual(format_interval(60), '01:00')
        self.assertEqual(format_interval(6160), '1:42:40')
        self.assertEqual(format_interval(238113), '66:08:33')

    def test_eval_progress_returns_none_on_failure(self):
        # given a match in the string, should eval the result
        regex = r'(\d+)/(\d+)$'
        processor = ProcessController(regex, r'x[0] *^/* x[1]', False, 'utf-8')
        match = re.search(regex, '50/50')
        self.assertIsNone(processor._eval_progress(match))
