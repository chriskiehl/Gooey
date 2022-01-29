import sys
import unittest
from copy import deepcopy

from gooey import Events
from gooey.tests.harness import instrumentGooey
from gooey.tests import *

class TestLiveDynamicUpdates(unittest.TestCase):

    def test_validate_form(self):
        """
        Integration testing the Dynamic Validation features.
        """
        # Because it's a live test, nothing is mocked. This basic.py file
        # will be called via subprocess as part of the test. As such, we
        # grab both its path on disk (for use as a target for Gooey) as
        # well as its parser instance (so that we can bootstrap)
        from gooey.tests.dynamics.files import basic
        params = {
            'target': '{} -u {}'.format(sys.executable, basic.__file__),
            'use_events': [Events.VALIDATE_FORM],
        }
        with instrumentGooey(basic.make_parser(), **params) as (app, frame, gapp):
            # the parser has a single arg of type int.
            # We purposefully give it invalid input for the sake of the test.
            gapp.getActiveConfig().widgetsMap['foo'].setValue('not a number')
            # and make sure we're not somehow starting with an error
            self.assertEqual(gapp.getActiveFormState()[0]['error'], '')
            gapp.onStart()

            # All subprocess calls ultimately pump though wx's event queue
            # so we have to kick off the mainloop and let it run long enough
            # to let the subprocess complete and the event queue flush
            wx.CallLater(2500, app.ExitMainLoop)
            app.MainLoop()
            # after the subprocess call is complete, our UI should have
            # been updated with the data dynamically returned from the
            # basic.py invocation.
            self.assertIn('invalid literal', gapp.getActiveFormState()[0]['error'])


    def test_validate_form_without_errors(self):
        from gooey.tests.dynamics.files import basic
        params = {
            'target': '{} -u {}'.format(sys.executable, basic.__file__),
            'use_events': [Events.VALIDATE_FORM],
            # setting to false because it interferes with the test
            'show_success_modal': False
        }
        with instrumentGooey(basic.make_parser(), **params) as (app, frame, gapp):
            gapp.getActiveConfig().widgetsMap['foo'].setValue('10')  # valid int
            self.assertEqual(gapp.getActiveFormState()[0]['error'], '')
            gapp.onStart()

            wx.CallLater(2500, app.ExitMainLoop)
            app.MainLoop()
            # no errors blocked the run, so we should have executed and finished.
            # we're now on the success screen.
            self.assertEqual(gapp.state['image'], gapp.state['images']['successIcon'])
            # and indeed no errors were written to the UI
            self.assertEqual(gapp.getActiveFormState()[0]['error'], '')
            # and we find the expected output written to the console
            # rather than some unexpected error
            self.assertIn('DONE', frame.FindWindowByName("console").getText())


    def test_lifecycle_handlers(self):
        cases = [
            {'input': 'happy path', 'expected_stdout': 'DONE', 'expected_update': 'success'},
            {'input': 'fail', 'expected_stdout': 'EXCEPTION', 'expected_update': 'error'}
        ]
        from gooey.tests.dynamics.files import lifecycles
        params = {
            'target': '{} -u {}'.format(sys.executable, lifecycles.__file__),
            'use_events': [Events.ON_SUCCESS, Events.ON_ERROR],
            'show_success_modal': False,
            'show_failure_modal': False
        }
        for case in cases:
            with self.subTest(case):
                with instrumentGooey(lifecycles.make_parser(), **params) as (app, frame, gapp):
                    gapp.getActiveConfig().widgetsMap['foo'].setValue(case['input'])
                    gapp.onStart()
                    # give everything a chance to run
                    wx.CallLater(2000, app.ExitMainLoop)
                    app.MainLoop()
                    # `lifecycle.py` is set up to raise an exception for certain inputs
                    # so we check that we find our expected stdout here
                    console = frame.FindWindowByName("console")
                    self.assertIn(case['expected_stdout'], console.getText())

                    # Now, based on what happened during the run (success/exception) our
                    # respective lifecycle handler should have been called. These are
                    # configured to update the form field in the UI with a relevant value.
                    # Thus we we're checking here to see that out input has changed, and now
                    # matches the value we expect from the handler
                    textfield = gapp.getActiveFormState()[0]
                    print(case['expected_update'], textfield['value'])
                    self.assertEqual(case['expected_update'], textfield['value'])

