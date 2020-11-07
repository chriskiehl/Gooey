import re
import unittest

from gooey.tests import *

from gooey.gui.util.time import get_current_time,get_elapsed_time,estimate_time_remaining,format_interval


class TestTimeUtil(unittest.TestCase):
    def test_time_elapsed(self):
        # Check that time elapsed is greater than zero
        _start_time = get_current_time()
        elapsed = get_elapsed_time(_start_time)
        self.assertGreater(elapsed,0)

    def test_time_remaining(self):
        # Check that time elapsed is greater than zero
        _start_time = get_current_time()
        remaining = estimate_time_remaining(30,_start_time)
        self.assertGreater(remaining,0)

    def test_current_time(self):
        # Test that current time is greater than zero
        _start_time = get_current_time()
        self.assertGreater(_start_time,0)

    
    def test_format_interval(self):
        # Test same as TQDM https://github.com/tqdm/tqdm/blob/0cd9448b2bc08125e74538a2aea6af42ee1a7b6f/tqdm/tests/tests_tqdm.py#L234
        # but in unittest form

        self.assertEqual(format_interval(60), '01:00')
        self.assertEqual(format_interval(6160), '1:42:40')
        self.assertEqual(format_interval(238113), '66:08:33')
