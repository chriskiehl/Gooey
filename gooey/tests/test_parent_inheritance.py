import argparse
import unittest

from gooey import GooeyParser
from gooey.tests import *

class TestParentInheritance(unittest.TestCase):

    def test_parent_arguments_exist_in_child(self):
        """
        Verifies that the parents parameter is honoured.
        """
        base_parser = GooeyParser(add_help=False)
        base_parser.add_argument("a_file", widget="FileChooser")

        parser = GooeyParser(parents=[base_parser])
        parser.add_argument("b_file", widget="DirChooser")

        found = 0
        for action in parser._actions:
            if action.dest == "a_file":
                found += 1
            elif action.dest == "b_file":
                found += 1

        self.assertEqual(2, found, "Did not find 2 expected arguments, found " + str(found))
        self.assertEqual(parser.widgets["a_file"], "FileChooser")
        self.assertEqual(parser.widgets["b_file"], "DirChooser")

    def test_parent_arguments_are_not_overridden(self):
        """
        Verifies that the same named argument in a parent and child parser is accepted, and only the child
        parser survives.
        """
        # Verify how vanilla argparse works
        base_parser = argparse.ArgumentParser(add_help=False)
        action1 = base_parser.add_argument("a_file", default="a")

        parser = argparse.ArgumentParser(parents=[base_parser])
        action2 = parser.add_argument("a_file", default="b")

        self._verify_duplicate_parameters(action1, action2, parser)
        # So a child can't override a parent - this isn't textbook inheritance

        # Run the same test on GooeyParser
        base_parser = GooeyParser(add_help=False)
        action1 = base_parser.add_argument("a_file", widget="FileChooser", default="a")

        parser = GooeyParser(parents=[base_parser])
        action2 = parser.add_argument("a_file", widget="DirChooser", default="b")

        self._verify_duplicate_parameters(action1, action2, parser)
        self.assertEqual(parser.widgets["a_file"], "FileChooser")

    def test_parent_mutually_exclusive_groups_exist_in_child(self):
        """
        Verifies that mutually exclusive groups on a parent are inherited, along with their widgets.
        """
        # Case: A parent GooeyParser has a required mutually exclusive group of two arguments,
        # one of which has a widget, and a child GooeyParser inherits from it.
        # Expected: The child has one mutually exclusive group with the same arguments, it is
        # still required, and the widget is carried over.
        base_parser = GooeyParser(add_help=False)
        mutex = base_parser.add_mutually_exclusive_group(required=True)
        mutex.add_argument("--one", action="store_true", widget="CheckBox")
        mutex.add_argument("--two", action="store_true")

        parser = GooeyParser(parents=[base_parser])

        expected_mutex_count = 1
        expected_mutex_dests = ["one", "two"]
        expected_mutex_required = True
        expected_widget = "CheckBox"
        actual_mutex_count = len(parser._mutually_exclusive_groups)
        assert actual_mutex_count == expected_mutex_count
        actual_mutex = parser._mutually_exclusive_groups[0]
        actual_mutex_dests = [action.dest for action in actual_mutex._group_actions]
        actual_mutex_required = actual_mutex.required
        actual_widget = parser.widgets["one"]
        assert actual_mutex_dests == expected_mutex_dests
        assert actual_mutex_required == expected_mutex_required
        assert actual_widget == expected_widget

    def test_duplicates_on_same_parser_are_ignored(self):
        """
        Verify that adding duplicate named arguments works the same in argparse and Gooey.
        Assuming the behaviour of the "default" parameter is a good match for the "widget" parameter.
        """

        # Verify how vanilla argparse works
        parser = argparse.ArgumentParser()
        action1 = parser.add_argument("a_file", default="a")
        action2 = parser.add_argument("a_file", default="b")

        self._verify_duplicate_parameters(action1, action2, parser)

        # Run the same test on GooeyParser
        parser = GooeyParser()
        action1 = parser.add_argument("a_file", default="a", widget="FileChooser")
        action2 = parser.add_argument("a_file", default="b", widget="DirChooser")

        self._verify_duplicate_parameters(action1, action2, parser)
        self.assertEqual(parser.widgets["a_file"], "FileChooser")

    def _verify_duplicate_parameters(self, action1, action2, parser):
        """
        Verify two parameters named a_file exist and the default value is "a".
        """
        found = 0
        for action in parser._actions:
            if action.dest == "a_file":
                found += 1
        self.assertEqual(2, found, "Expected a both actions handling a_file but got " + str(found))
        self.assertEqual(parser.get_default("a_file"), "a")
        self.assertNotEqual(action1, action2)