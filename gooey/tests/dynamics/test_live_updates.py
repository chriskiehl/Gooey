import sys
import unittest

from gooey import Events
from gooey.tests.harness import instrumentGooey
from gooey.tests import *

class TestLiveDynamicUpdates(unittest.TestCase):
    pass
    # def test_validate_form(self):
    #     """
    #     Integration testing the Dynamic Validation features.
    #     """
    #     # Because it's a live test, nothing is mocked. This basic.py file
    #     # will be called via subprocess as part of the test. As such, we
    #     # grab both its path on disk (for use as a target for Gooey) as
    #     # well as its parser instance (so that we can bootstrap)
    #     from gooey.tests.dynamics.files import basic
    #     params = {
    #         'target': '{} -u {}'.format(sys.executable, basic.__file__),
    #         'use_events': [Events.VALIDATE_FORM],
    #     }
    #     with instrumentGooey(basic.parser, **params) as (app, gapp):
    #         # the parser has a single arg of type int.
    #         # We purposefully give it invalid input for the sake of the test.
    #         gapp.configs[0].widgetsMap['foo'].setValue('not a number')
    #         gapp.onStart()
    #         # after the subprocess call is complete, our UI should have
    #         # been updated with the data dynamically returned from the
    #         # basic.py invocation.
    #         self.assertIn(
    #             'invalid literal for int()',
    #             gapp.configs[0].widgetsMap['foo'].error.Label
    #         )
    #
    #
    # def test_validate_form_without_errors(self):
    #     from gooey.tests.dynamics.files import basic
    #     params = {
    #         'target': '{} -u {}'.format(sys.executable, basic.__file__),
    #         'use_events': [Events.VALIDATE_FORM]
    #     }
    #     with instrumentGooey(basic.parser, **params) as (app, gapp):
    #         valid_int = '10'
    #         gapp.configs[0].widgetsMap['foo'].setValue(valid_int)
    #         gapp.onStart()
    #         # because we supplied a valid int, there should have been
    #         # no validation errors returned
    #         self.assertEqual(
    #             gapp.configs[0].widgetsMap['foo'].error.Label,
    #             ''
    #         )
