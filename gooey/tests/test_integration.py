import json
import sys
import time
import unittest
from concurrent import futures
from os import path

from gooey.gui import application
from gooey.gui.lang.i18n import _
from gooey.gui.util.freeze import getResourcePath
from gooey.gui.util.quoting import quote


class TestGooeyIntegration(unittest.TestCase):
    """
    A few quick integration tests that exercise Gooey's various run modes

    WX Python needs to control the main thread. So, in order to simulate a user
    running through the system, we have to execute the actual assertions in a
    different thread
    """
    LOCAL_DIR = path.dirname(__file__)

    def performTest(self, configPath, assertionFunction):
        """
        Primary test harness.

        Instantiates the WX App, and spawns the threads
        required to make assertions against it
        """
        with open(configPath, 'r') as f:
            build_spec = json.loads(f.read())
            # swaps the absolute path stored by Gooey at write time
            # for a relative one based on our current test location
            target_pyfile = path.split(build_spec['target'].replace('"', ''))[-1]
            file_path = path.join(path.dirname(__file__), target_pyfile)
            run_cmd = '{} -u {}'.format(quote(sys.executable), quote(file_path))
            build_spec['language_dir'] = getResourcePath('languages')
            build_spec['target'] = run_cmd

        app = application.build_app(build_spec=build_spec)
        executor = futures.ThreadPoolExecutor(max_workers=1)
        testResult = executor.submit(assertionFunction, app, build_spec)
        app.MainLoop()
        testResult.result()
        # some extra padding time between starting/stopping the wx App
        app.Destroy()
        time.sleep(1)


    def test_gooeyNormalRun(self):
        """ Tests the happy path through the default run mode of Gooey """
        self.performTest(path.join(self.LOCAL_DIR, 'gooey_config__normal.json'), self.gooeySanityTest)

    def test_gooeySubparserMode(self):
        """ Tests the happy path through the subparser run mode of Gooey """
        self.performTest(path.join(self.LOCAL_DIR, 'gooey_config__subparser.json'), self.gooeySanityTest)

    def test__gooeyAutoStart(self):
        """Verifies that issue #201 doesn't regress and auto_start skips the config
        screen and hops right into the client's program"""
        self.performTest(path.join(self.LOCAL_DIR, 'gooey_config__autostart.json'), self.verifyAutoStart)

    def test__gooeyValidation(self):
        """Verifies that custom validation routines supplied via gooey_options prevents
        the user from advancing past the configuration page when they fail"""
        self.performTest(path.join(self.LOCAL_DIR, 'gooey_config__autostart.json'), self.verifyValidators)


    def verifyValidators(self, app, buildSpec):
        time.sleep(1)
        try:
            app.TopWindow.onStart()
            # we should still be on the configuration page due to a validation fail
            title = app.TopWindow.header._header.GetLabel()
            subtitle = app.TopWindow.header._subheader.GetLabel()
            self.assertNotEqual(title, buildSpec['program_name'])
            self.assertNotEqual(subtitle, buildSpec['program_description'])
        except:
            app.TopWindow.Destroy()
            raise
        else:
            app.TopWindow.Destroy()
            return None

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
            app.TopWindow.Destroy()
            return None


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
        except:
            app.TopWindow.Destroy()
            raise
        else:
            app.TopWindow.Destroy()
            return None


if __name__ == '__main__':
    unittest.main()






