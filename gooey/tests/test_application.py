import os
import sys
import unittest
from argparse import ArgumentParser
from collections import namedtuple
from unittest.mock import patch
from unittest.mock import MagicMock

import wx

from gooey import GooeyParser
from python_bindings import constants
from tests.harness import instrumentGooey

from gooey.tests import *

class TestGooeyApplication(unittest.TestCase):

    def testFullscreen(self):
        parser = self.basicParser()
        for shouldShow in [True, False]:
            with self.subTest('Should set full screen: {}'.format(shouldShow)):
                with instrumentGooey(parser, fullscreen=shouldShow) as (app, gapp):
                    self.assertEqual(gapp.IsFullScreen(), shouldShow)


    @patch("gui.containers.application.modals.confirmForceStop")
    def testGooeyRequestsConfirmationWhenShowStopWarningModalTrue(self, mockModal):
        """
        When show_stop_warning=False, Gooey should immediately kill the
        running program without additional user confirmation.

        Otherwise, Gooey should show a confirmation modal and, dependending on the
        user's choice, either do nothing or kill the running program.
        """
        Case = namedtuple('Case', ['show_warning', 'shouldSeeConfirm', 'userChooses', 'shouldHaltProgram'])
        testcases = [
            Case(show_warning=True, shouldSeeConfirm=True, userChooses=True, shouldHaltProgram=True),
            Case(show_warning=True, shouldSeeConfirm=True, userChooses=False, shouldHaltProgram=False),
            Case(show_warning=False, shouldSeeConfirm=False, userChooses='N/A', shouldHaltProgram=True),
        ]

        for case in testcases:
            mockModal.reset_mock()
            parser = self.basicParser()
            with instrumentGooey(parser, show_stop_warning=case.show_warning) as (app, gapp):
                mockClientRunner = MagicMock()
                mockModal.return_value = case.userChooses
                gapp.clientRunner = mockClientRunner

                gapp.onStopExecution()

                if case.shouldSeeConfirm:
                    mockModal.assert_called()
                else:
                    mockModal.assert_not_called()

                if case.shouldHaltProgram:
                    mockClientRunner.stop.assert_called()
                else:
                    mockClientRunner.stop.assert_not_called()

    @patch("gui.containers.application.modals.confirmForceStop")
    def testOnCloseShutsDownActiveClients(self, mockModal):
        """
        Issue 592: Closing the UI should clean up any actively running programs
        """
        parser = self.basicParser()
        with instrumentGooey(parser) as (app, gapp):
            gapp.clientRunner = MagicMock()
            gapp.destroyGooey = MagicMock()
            # mocking that the user clicks "yes shut down" in the warning modal
            mockModal.return_value = True
            gapp.onClose()

            mockModal.assert_called()
            gapp.destroyGooey.assert_called()


    def testTerminalColorChanges(self):
        ## Issue #625 terminal panel color wasn't being set due to a typo
        parser = self.basicParser()
        expectedColors = [(255, 0, 0, 255), (255, 255, 255, 255), (100, 100, 100,100)]
        for expectedColor in expectedColors:
            with instrumentGooey(parser, terminal_panel_color=expectedColor) as (app, gapp):
                foundColor = gapp.console.GetBackgroundColour()
                self.assertEqual(tuple(foundColor), expectedColor)


    def testFontWeightsGetSet(self):
        ## Issue #625 font weight wasn't being correctly passed to the terminal
        for weight in [constants.FONTWEIGHT_LIGHT, constants.FONTWEIGHT_BOLD]:
            parser = self.basicParser()
            with instrumentGooey(parser, terminal_font_weight=weight) as (app, gapp):
                terminal = gapp.console.textbox
                self.assertEqual(terminal.GetFont().GetWeight(), weight)

    def testSubparserProgHasNoColorCodes(self):
        # Python 3.14+ now automatically colors the output text of argparse
        # when run from a terminal. This test ensures that Gooey's subcommand
        # sidebar names are always plain text and do not include ANSI color codes.
        testcases = [
            # C1: Color output is disabled.
            # Expected: Prog is plain text with no ANSI escape codes.
            ({'PYTHON_COLORS': '0'}, 'program subcommand'),
            # C2: Color output is enabled.
            # Expected: Prog is plain text with no ANSI escape codes.
            ({'PYTHON_COLORS': '1'}, 'program subcommand'),
        ]
        for input_environment, expected_prog in testcases:
            with self.subTest(input_environment):
                with patch.dict(os.environ, input_environment):
                    parser = GooeyParser(prog='program')
                    subparsers = parser.add_subparsers(dest='command')
                    subcommand_parser = subparsers.add_parser('subcommand')
                actual_prog = subcommand_parser.prog
                self.assertEqual(actual_prog, expected_prog)

    def testRichtextControlsColorsConsoleText(self):
        # The console only turns ANSI color codes into colored text when
        # richtext_controls=True. Otherwise the text keeps the default
        # terminal font color. Each case writes "hello" wrapped in the
        # 256-color code for green and reads back the color of "hello".
        testcases = [
            # C1: richtext_controls is not set (default False).
            # Expected: "hello" stays in the default black.
            ({}, '#000000'),
            # C2: richtext_controls is explicitly False.
            # Expected: "hello" stays in the default black.
            ({'richtext_controls': False}, '#000000'),
            # C3: richtext_controls is True.
            # Expected: "hello" is green.
            ({'richtext_controls': True}, '#008000'),
        ]
        for input_options, expected_hello_color in testcases:
            with self.subTest(input_options):
                parser = self.basicParser()
                with instrumentGooey(parser, **input_options) as (app, gapp):
                    gapp.console.appendText('\x1b[38;5;2mhello\x1b[0m\n')
                    inside_hello_position = gapp.console.getText().find('hello') + 1
                    hello_style = wx.TextAttr()
                    gapp.console.textbox.GetStyle(inside_hello_position, hello_style)
                    actual_hello_color = hello_style.GetTextColour().GetAsString(wx.C2S_HTML_SYNTAX)
                self.assertEqual(actual_hello_color, expected_hello_color)


    def basicParser(self):
        parser = ArgumentParser()
        parser.add_argument('--foo')
        return parser




if __name__ == '__main__':
    unittest.main()