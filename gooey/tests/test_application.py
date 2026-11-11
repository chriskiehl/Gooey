import os
import sys
import unittest
from argparse import ArgumentParser
from collections import namedtuple
from unittest.mock import patch
from unittest.mock import MagicMock

import colored
import wx

from gooey import GooeyParser
from gooey.gui import application
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
        # The console only turns 256-color ANSI codes (like \x1b[38;5;2m) into
        # colored text when richtext_controls=True. Otherwise the codes are
        # shown as plain text and the text keeps the terminal_font_color.
        # Each case writes "hello" wrapped in the 256-color code for green,
        # then reads back the console text and the color of "hello".
        testcases = [
            # C1: richtext_controls is not set (default False).
            # Expected: The color codes stay in the text as characters and
            # "hello" stays in the default black.
            ({}, '\x1b[38;5;2mhello\x1b[0m\n', '#000000'),
            # C2: richtext_controls is explicitly False.
            # Expected: As above, the color codes stay in the text as 
            # characters and "hello" stays in the default black.
            ({'richtext_controls': False}, '\x1b[38;5;2mhello\x1b[0m\n', '#000000'),
            # C3: richtext_controls is True.
            # Expected: The color codes are removed and "hello" is green.
            ({'richtext_controls': True}, 'hello\n', '#008000'),
        ]
        for input_options, expected_console_text, expected_hello_color in testcases:
            with self.subTest(input_options):
                parser = self.basicParser()
                with instrumentGooey(parser, **input_options) as (app, gapp):
                    gapp.console.appendText('\x1b[38;5;2mhello\x1b[0m\n')
                    actual_console_text = gapp.console.getText()
                    inside_hello_position = actual_console_text.find('hello') + 1
                    hello_style = wx.TextAttr()
                    gapp.console.textbox.GetStyle(inside_hello_position, hello_style)
                    actual_hello_color = hello_style.GetTextColour().GetAsString(wx.C2S_HTML_SYNTAX)
                self.assertEqual(actual_console_text, expected_console_text)
                self.assertEqual(actual_hello_color, expected_hello_color)

    def testRichtextControlsStylesConsoleText(self):
        # The console turns the ANSI bold and underline codes, and the codes
        # that end them, into styled text when richtext_controls=True. Each
        # case writes "hello" after a sequence of codes, then reads back the
        # console text and the style attributes of "hello" that the case checks.
        testcases = [
            # C1: Bold code (1).
            # Expected: The codes are removed and "hello" is bold, not underlined.
            ('\x1b[1mhello\n', {'bold': True, 'underlined': False}),
            # C2: Underline code (4).
            # Expected: The codes are removed and "hello" is underlined, not bold.
            ('\x1b[4mhello\n', {'bold': False, 'underlined': True}),
            # C3: Bold code (1) followed by the end bold code (21).
            # Expected: The codes are removed and "hello" is not bold.
            ('\x1b[1m\x1b[21mhello\n', {'bold': False}),
            # C4: Underline code (4) followed by the end underline code (24).
            # Expected: The codes are removed and "hello" is not underlined.
            ('\x1b[4m\x1b[24mhello\n', {'underlined': False}),
        ]
        for input_text, expected_hello_style in testcases:
            with self.subTest(input_text):
                parser = self.basicParser()
                with instrumentGooey(parser, richtext_controls=True) as (app, gapp):
                    gapp.console.appendText(input_text)
                    actual_console_text = gapp.console.getText()
                    hello_style = self.getConsoleTextStyle(gapp, 'hello')
                actual_hello_style = {name: hello_style[name] for name in expected_hello_style}
                self.assertEqual(actual_console_text, 'hello\n')
                self.assertEqual(actual_hello_style, expected_hello_style)

    def testRichtextControlsResetRestoresDefaultStyle(self):
        # The ANSI reset code (0) ends every style, so text after it looks
        # the same as text written before any codes.
        parser = self.basicParser()
        with instrumentGooey(parser, richtext_controls=True) as (app, gapp):
            gapp.console.appendText('plain \x1b[1m\x1b[4m\x1b[38;5;2m\x1b[0mhello\n')
            actual_console_text = gapp.console.getText()
            expected_hello_style = self.getConsoleTextStyle(gapp, 'plain')
            actual_hello_style = self.getConsoleTextStyle(gapp, 'hello')
        self.assertEqual(actual_console_text, 'plain hello\n')
        self.assertEqual(actual_hello_style, expected_hello_style)

    def testRichtextControlsRendersColoredLibraryOutput(self):
        # Output styled with the colored library, which the richtext docs
        # recommend, renders in the console with both colored 1.x and 2.x.
        # Version 1.4 and later only add codes when writing to a terminal, so
        # FORCE_COLOR is set here as a program run by Gooey needs to do.
        # Each case writes "hello" styled by colored, then reads back the
        # console text and the style attributes of "hello" that the case checks.
        testcases = [
            # C1: Foreground color by name.
            # Expected: The codes are removed and "hello" is green.
            (lambda: colored.fg('green'), {'color': '#008000'}),
            # C2: Bold attribute by name.
            # Expected: The codes are removed and "hello" is bold, not underlined.
            (lambda: colored.attr('bold'), {'bold': True, 'underlined': False}),
            # C3: Underline attribute by code.
            # Expected: The codes are removed and "hello" is underlined, not bold.
            (lambda: colored.attr(4), {'bold': False, 'underlined': True}),
            # C4: Foreground color and bold attribute combined with +.
            # Expected: The codes are removed and "hello" is bold and red.
            (lambda: colored.fg('red') + colored.attr('bold'), {'bold': True, 'color': '#800000'}),
        ]
        for input_style, expected_hello_style in testcases:
            with patch.dict(os.environ, {'FORCE_COLOR': '1'}):
                styled_hello = colored.stylize('hello', input_style()) + '\n'
            with self.subTest(styled_hello):
                parser = self.basicParser()
                with instrumentGooey(parser, richtext_controls=True) as (app, gapp):
                    gapp.console.appendText(styled_hello)
                    actual_console_text = gapp.console.getText()
                    hello_style = self.getConsoleTextStyle(gapp, 'hello')
                actual_hello_style = {name: hello_style[name] for name in expected_hello_style}
                self.assertEqual(actual_console_text, 'hello\n')
                self.assertEqual(actual_hello_style, expected_hello_style)

    def testDarkModeColorsWindow(self):
        # The window, header, and footer use dark backgrounds when the
        # system is in dark mode, so native text such as button labels,
        # which the system draws in white, stays readable. Each case builds
        # the window and reads back its background colors.
        testcases = [
            # C1: Light mode.
            # Expected: The light backgrounds Gooey has always used.
            (False, {'body': '#F0F0F0', 'header': '#FFFFFF', 'footer': '#F0F0F0'}),
            # C2: Dark mode.
            # Expected: Dark backgrounds.
            (True, {'body': '#292A31', 'header': '#19191D', 'footer': '#292A31'}),
        ]
        for input_dark_mode, expected_backgrounds in testcases:
            with self.subTest(dark_mode=input_dark_mode):
                parser = self.basicParser()
                with instrumentGooey(parser, dark_mode=input_dark_mode) as (app, gapp):
                    actual_backgrounds = {
                        'body': gapp.GetBackgroundColour().GetAsString(wx.C2S_HTML_SYNTAX),
                        'header': gapp.header.GetBackgroundColour().GetAsString(wx.C2S_HTML_SYNTAX),
                        'footer': gapp.footer.GetBackgroundColour().GetAsString(wx.C2S_HTML_SYNTAX),
                    }
                self.assertEqual(actual_backgrounds, expected_backgrounds)

    def testGetAppReusesRunningApp(self):
        # Gooey creates its wx.App before building the window settings so it
        # can check for dark mode, and must then reuse that App instead of
        # creating a second one.
        # Expected: The App that is already running is returned.
        actual_app = application.get_app()
        self.assertIs(actual_app, wx.GetApp())

    def getConsoleTextStyle(self, gapp, text):
        inside_text_position = gapp.console.getText().find(text) + 1
        text_style = wx.TextAttr()
        gapp.console.textbox.GetStyle(inside_text_position, text_style)
        return {
            'bold': text_style.GetFontWeight() == wx.FONTWEIGHT_BOLD,
            'underlined': text_style.GetFontUnderlined(),
            'color': text_style.GetTextColour().GetAsString(wx.C2S_HTML_SYNTAX),
        }


    def basicParser(self):
        parser = ArgumentParser()
        parser.add_argument('--foo')
        return parser




if __name__ == '__main__':
    unittest.main()