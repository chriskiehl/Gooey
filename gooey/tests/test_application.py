import sys
import unittest
from argparse import ArgumentParser
from collections import namedtuple
from unittest.mock import patch
from unittest.mock import MagicMock

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


    def basicParser(self):
        parser = ArgumentParser()
        parser.add_argument('--foo')
        return parser




if __name__ == '__main__':
    unittest.main()