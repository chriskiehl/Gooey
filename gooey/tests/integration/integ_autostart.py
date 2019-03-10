import time
import unittest

from gooey.gui.lang.i18n import _
from tests.integration.programs import auto_start as auto_start_module


class TestGooeyIntegration(unittest.TestCase):

    def test__gooeyAutoStart(self):
        """Verifies that issue #201 doesn't regress and auto_start skips the config
        screen and hops right into the client's program"""
        from gooey.tests.integration import runner
        runner.run_integration(auto_start_module, self.verifyAutoStart, auto_start=True)

    def verifyAutoStart(self, app, buildSpec):
        """
        When the auto_start flag == True Gooey should skip the
        configuration screen
        """
        time.sleep(1)
        try:
            # Gooey should NOT be showing the name/description headers
            # present on the config page
            title = app.TopWindow.header._header.GetLabel()
            subtitle = app.TopWindow.header._subheader.GetLabel()
            self.assertNotEqual(title, buildSpec['program_name'])
            self.assertNotEqual(subtitle, buildSpec['program_description'])

            # Gooey should be showing the console messages straight away
            # without manually starting the program
            title = app.TopWindow.header._header.GetLabel()
            subtitle = app.TopWindow.header._subheader.GetLabel()
            self.assertEqual(title,_("running_title"))
            self.assertEqual(subtitle, _('running_msg'))

            # Wait for Gooey to swap the header to the final screen
            while app.TopWindow.header._header.GetLabel() == _("running_title"):
                time.sleep(.1)

            # verify that we've landed on the success screen
            title = app.TopWindow.header._header.GetLabel()
            subtitle = app.TopWindow.header._subheader.GetLabel()
            self.assertEqual(title, _("finished_title"))
            self.assertEqual(subtitle, _('finished_msg'))


            # and that output was actually written to the console
            self.assertIn("Success", app.TopWindow.console.textbox.GetValue())
        except:
            app.TopWindow.Destroy()
            raise
        else:
            import wx
            wx.CallAfter(app.TopWindow.Destroy)
            return None




if __name__ == '__main__':
    unittest.main()






