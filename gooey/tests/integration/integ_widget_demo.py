import time
import unittest

import wx
from gooey.gui.lang.i18n import _
from tests.integration.programs import all_widgets as all_widgets_module


class TestGooeyIntegration99(unittest.TestCase):


    def test_gooeyNormalRun(self):
        """ Tests the happy path through the default run mode of Gooey """
        from gooey.tests.integration import runner
        runner.run_integration(all_widgets_module, self.gooeySanityTest)


    def gooeySanityTest(self, app, buildSpec):
        time.sleep(1)
        try:
            # Check out header is present and showing data
            title = app.TopWindow.header._header.GetLabel()
            subtitle = app.TopWindow.header._subheader.GetLabel()
            self.assertEqual(title, buildSpec['program_name'])
            self.assertEqual(subtitle, buildSpec['program_description'])

            # switch to the run screen
            app.TopWindow.onStart()

            # Should find the expected test in the header
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
            time.sleep(1)
        except:
            app.TopWindow.Destroy()
            raise
        else:
            wx.CallAfter(app.TopWindow.Destroy)
            return None


if __name__ == '__main__':
    unittest.main()






