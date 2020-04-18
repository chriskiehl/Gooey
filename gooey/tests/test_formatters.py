import argparse
import os
import shlex
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

    def test_multifilechooser_formatter(self):
        """
        Should return files (quoted), separated by spaces if there is more
        than one, preceeded by optional command if the argument is optional.

        Assumes the argument has been created with some form of nargs, which
        only makes sense for possibly choosing multiple values.
        """

        # Helper function to generalize the variants we need to test
        def multifilechooser_helper(names):
            # Note that the MultiFileChooser widget produces a single string with
            # paths separated by os.pathsep.
            if names:
                prefix = names[0] + ' '
            else:
                prefix = ''

            expected_outputs = [
                (names, None, ''),
                (names, prefix + '"abc"', 'abc'),
                (names, prefix + '"abc" "def"', os.pathsep.join(['abc', 'def'])),
                # paths with spaces
                (names, prefix + '"a b c"', 'a b c'),
                (names, prefix + '"a b c" "d e f"', os.pathsep.join(['a b c', 'd e f'])),
            ]

            for commands, expected, widget_result in expected_outputs:
                result = formatters.multiFileChooser({'commands': commands}, widget_result)
                self.assertEqual(result, expected)
                # make sure that argparse actually accepts it as valid.
                if result:
                    parser = argparse.ArgumentParser()
                    if not names:
                        names = ["file"]
                    parser.add_argument(names[0], nargs='+')
                    parser.parse_args(shlex.split(result))

        # Positional argument, with nargs
        multifilechooser_helper([])

        # Optional argument, with nargs
        multifilechooser_helper(["-f", "--file"])
