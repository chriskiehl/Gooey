import time
import unittest

from tests.integration.programs import validations as validations_module


class TestGooeyIntegration(unittest.TestCase):
    """
    A few quick integration tests that exercise Gooey's various run modes

    WX Python needs to control the main thread. So, in order to simulate a user
    running through the system, we have to execute the actual assertions in a
    different thread
    """

    def test__gooeyValidation(self):
        """Verifies that custom validation routines supplied via gooey_options prevents
        the user from advancing past the configuration page when they fail"""
        from gooey.tests.integration import runner
        runner.run_integration(validations_module, self.verifyValidators)


    def verifyValidators(self, app, buildSpec):
        time.sleep(1)
        try:
            app.TopWindow.onStart()
            title = app.TopWindow.header._header.GetLabel()
            subtitle = app.TopWindow.header._subheader.GetLabel()
            self.assertNotEqual(title, buildSpec['program_name'])
            self.assertNotEqual(subtitle, buildSpec['program_description'])
        except:
            app.TopWindow.Destroy()
            raise
        else:
            import wx
            wx.CallAfter(app.TopWindow.Destroy)
            return None



if __name__ == '__main__':
    unittest.main()






