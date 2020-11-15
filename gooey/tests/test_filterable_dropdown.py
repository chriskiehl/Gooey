import unittest
from argparse import ArgumentParser
from collections import namedtuple
from unittest.mock import patch
import wx
from gooey.tests import *

from gooey.tests.harness import instrumentGooey
from gooey import GooeyParser


class TestGooeyFilterableDropdown(unittest.TestCase):

    def make_parser(self, **kwargs):
        parser = GooeyParser(description='description')
        parser.add_argument('--dropdown', widget='FilterableDropdown', **kwargs)
        return parser

    def test_input_spawns_popup(self):
        parser = self.make_parser(choices=['alpha1', 'alpha2', 'beta', 'gamma'])
        with instrumentGooey(parser) as (app, gooeyApp):
            dropdown = gooeyApp.configs[0].reifiedWidgets[0]

            event = wx.CommandEvent(wx.wxEVT_TEXT, wx.Window.NewControlId())
            event.SetEventObject(dropdown.widget.GetTextCtrl())

            dropdown.widget.GetTextCtrl().ProcessEvent(event)
            self.assertTrue(
                dropdown.model.suggestionsVisible,
                dropdown.listbox.IsShown()
            )

    def test_arrow_key_selection_cycling(self):
        """
        Testing that the up/down arrow keys spawn the dropdown
        and cycle through its options wrapping around as needed.
        """
        Scenario = namedtuple('Scenario', [
            'key', 'expectVisible', 'expectedSelection', 'expectedDisplayValue'])

        choices = ['alpha', 'beta']
        # no text entered yet
        initial = Scenario(None, False, -1, '')
        scenarios = [
            # cycling down
            [
            Scenario(wx.WXK_DOWN, True, -1, ''),
            Scenario(wx.WXK_DOWN, True, 0, 'alpha'),
            Scenario(wx.WXK_DOWN, True, 1, 'beta'),
            # wraps around to top
            Scenario(wx.WXK_DOWN, True, 0, 'alpha')
        ],  # cycling up
            [
            Scenario(wx.WXK_UP, True, -1, ''),
            Scenario(wx.WXK_UP, True, 1, 'beta'),
            Scenario(wx.WXK_UP, True, 0, 'alpha'),
            # wraps around to top
            Scenario(wx.WXK_UP, True, 1, 'beta'),
        ]]

        for actions in scenarios:
            parser = self.make_parser(choices=choices)
            with instrumentGooey(parser) as (app, gooeyApp):
                dropdown = gooeyApp.configs[0].reifiedWidgets[0]
                # sanity check we're starting from our known initial state
                self.assertEqual(dropdown.model.suggestionsVisible, initial.expectVisible)
                self.assertEqual(dropdown.model.displayValue, initial.expectedDisplayValue)
                self.assertEqual(dropdown.model.selectedSuggestion, initial.expectedSelection)

                for action in actions:
                    self.pressButton(dropdown, action.key)
                    self.assertEqual(
                        dropdown.model.suggestionsVisible,
                        dropdown.listbox.IsShown()
                    )
                    self.assertEqual(
                        dropdown.model.displayValue,
                        action.expectedDisplayValue
                    )
                    self.assertEqual(
                        dropdown.model.selectedSuggestion,
                        action.expectedSelection
                    )


    def enterText(self, dropdown, text):
        event = wx.CommandEvent(wx.wxEVT_TEXT, wx.Window.NewControlId())
        event.SetString(text)
        dropdown.widget.GetTextCtrl().ProcessEvent(event)

    def pressButton(self, dropdown, keycode):
        event = mockKeyEvent(keycode)
        dropdown.onKeyboardControls(event)


def mockKeyEvent(keycode):
    """
    Manually bypassing the setters as they don'y allow
    the non wx.wxXXX event variants by default.
    The internal WX post/prcess machinery doesn't handle key
    codes well for some reason, thus has to be mocked and
    manually passed to the relevant handler.
    """
    event = wx.KeyEvent()
    event.KeyCode = keycode
    return event


if __name__ == '__main__':
    unittest.main()
