import unittest
from importlib.metadata import version

import gooey


class TestVersion(unittest.TestCase):

    def test_version_matches_installed_package(self):
        # Test that __version__ is read from the installed package metadata
        # C1: Gooey is installed
        # Expected: __version__ equals the version of the installed package
        expected_version = version("Gooey")
        actual_version = gooey.__version__
        self.assertEqual(actual_version, expected_version)
        self.assertNotIn(actual_version, ("unknown", "0.0.0"))
