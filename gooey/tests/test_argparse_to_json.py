import json
import sys
import time
import unittest
from argparse import ArgumentParser
from concurrent import futures
from os import path
import wx

from gooey.gui import application
from gooey.gui.lang.i18n import _
from gooey.gui.util.freeze import getResourcePath
from gooey.gui.util.quoting import quote
from gooey.gui.components.widgets import Dropdown
from python_bindings import argparse_to_json
import os
from pprint import pprint

from util.functional import getin


class TestArgparse(unittest.TestCase):
    """
    TODO:
    """

    def test_json_iterable_conversion(self):
        """
        Issue #312 - tuples weren't being coerced to list during argparse
        conversion causing downstream issues when concatenating
        """
        # our original functionality accepted only lists as the choices arg
        parser = ArgumentParser()
        parser.add_argument("-foo", choices=['foo','bar', 'baz'])
        result = argparse_to_json.action_to_json(parser._actions[-1], "Dropdown", {})

        choices = result['data']['choices']
        self.assertTrue(isinstance(choices, list))
        self.assertEqual(choices, ['foo','bar', 'baz'])

        # Now we allow tuples as well.
        parser = ArgumentParser()
        parser.add_argument("-foo", choices=('foo','bar', 'baz'))
        result = argparse_to_json.action_to_json(parser._actions[-1], "Dropdown", {})

        choices = result['data']['choices']
        self.assertTrue(isinstance(choices, list))
        self.assertEqual(choices, ['foo','bar', 'baz'])


    def test_choice_string_cooersion(self):
        """
        Issue 321 - must coerce choice types to string to support wx.ComboBox
        """
        parser = ArgumentParser()
        parser.add_argument('--foo', choices=[1, 2, 3])
        choice_action = parser._actions[-1]
        result = argparse_to_json.action_to_json(choice_action, 'Dropdown', {})
        self.assertEqual(getin(result, ['data', 'choices']), ['1', '2', '3'])
        

