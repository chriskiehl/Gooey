import argparse
import unittest

from gooey.gui import formatters


class TestFormatters(unittest.TestCase):


    def test_counter_formatter(self):
        """
        Should return the first option repeated N times
        None if N is unspecified

        Issue #316 - using long-form argument caused formatter to produce incorrect output
        """
        expected_outputs = [
            (['-v', '--verbose'], '-v', 1),
            (['-v', '--verbose'], '-v -v', 2),
            (['-v', '--verbose'], '-v -v -v', 3),
            (['-v', '--verbose'], '', 0),
            # ensuring that log-forms are handled correctly
            (['--verbose', '-v'], '--verbose', 1),
            (['--verbose', '-v'], '--verbose --verbose', 2),
            (['--verbose', '-v'], '--verbose --verbose --verbose', 3),
            # single args
            (['-v'], '-v', 1),
            (['-v'], '-v -v', 2),
            (['--verbose'], '--verbose', 1),
            # bad inputs
            (['-v'], None, None),
            (['-v'], None, 'some-garbage'),
            (['-v'], None, 'af3gd'),
        ]

        for commands, expected, vebosity_level in expected_outputs:
            result = formatters.counter({'commands': commands}, vebosity_level)
            self.assertEqual(result, expected)
            # make sure that argparse actually accepts it as valid.
            if result:
                parser = argparse.ArgumentParser()
                parser.add_argument('-v', '--verbose', action='count')
                parser.parse_args(result.split())

