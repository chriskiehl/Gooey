import os
import unittest
from unittest.mock import patch

from gooey import GooeyParser
from gooey.tests import *


class TestGooeyParserSubparsers(unittest.TestCase):

    def test_subparser_prog_has_no_color_codes(self):
        # The subparser prog is shown as the subcommand name in Gooey's sidebar.
        # It must be plain text whether or not Python colorizes argparse output.
        testcases = [
            # C1: Color output is disabled.
            # Expected: Prog is the parent prog followed by the subcommand name.
            ({'PYTHON_COLORS': '0'}, 'demo curl'),
            # C2: Color output is forced, as when Gooey is launched from a terminal.
            # Expected: Prog is plain text with no ANSI escape codes.
            ({'PYTHON_COLORS': '1'}, 'demo curl'),
        ]
        for input_environment, expected_prog in testcases:
            with self.subTest(input_environment):
                with patch.dict(os.environ, input_environment):
                    parser = GooeyParser(prog='demo')
                    subparsers = parser.add_subparsers(dest='command')
                    curl_parser = subparsers.add_parser('curl')
                actual_prog = curl_parser.prog
                self.assertEqual(actual_prog, expected_prog)


if __name__ == '__main__':
    unittest.main()
