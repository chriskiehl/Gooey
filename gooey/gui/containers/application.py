"""
Primary orchestration and control point for Gooey.
"""

import sys

import wx
from wx.adv import TaskBarIcon

from gooey.gui import cli
from gooey.gui import events
from gooey.gui import seeder
from gooey.gui.components import modals
from gooey.gui.components.config import ConfigPage, TabbedConfigPage
from gooey.gui.components.console import Console
from gooey.gui.components.footer import Footer
from gooey.gui.components.header import FrameHeader
from gooey.gui.components.menubar import MenuBar
from gooey.gui.components.sidebar import Sidebar
from gooey.gui.components.tabbar import Tabbar
from gooey.gui.lang.i18n import _
from gooey.gui.processor import ProcessController
from gooey.gui.util.time import Timing
from gooey.gui.pubsub import pub
from gooey.gui.util import wx_util
from gooey.gui.util.wx_util import transactUI
from gooey.python_bindings import constants


class GooeyApplication(wx.Frame):
    """
    Main window for Gooey.
    """

    def __init__(self, buildSpec, *args, **kwargs):
        super(GooeyApplication, self).__init__(None, *args, **kwargs)
        self._state = {}
        self.buildSpec = buildSpec

        self.applyConfiguration()
        self.menu = MenuBar(buildSpec)
        self.SetMenuBar(self.menu)
        self.header = FrameHeader(self, buildSpec)
        self.configs = self.buildConfigPanels(self)
        self.navbar = self.buildNavigation()
        self.footer = Footer(self, buildSpec)
        self.console = Console(self, buildSpec)
        self.layoutComponent()
        self.timer = Timing(self)

        self.clientRunner = ProcessController(
            self.buildSpec.get('progress_regex'),
            self.buildSpec.get('progress_expr'),
            self.buildSpec.get('hide_progress_msg'),
            self.buildSpec.get('encoding'),
            self.buildSpec.get('requires_shell'),
        )

        pub.subscribe(events.WINDOW_START, self.onStart)
        pub.subscribe(events.WINDOW_RESTART, self.onStart)
        pub.subscribe(events.WINDOW_STOP, self.onStopExecution)
        pub.subscribe(events.WINDOW_CLOSE, self.onClose)
        pub.subscribe(events.WINDOW_CANCEL, self.onCancel)
        pub.subscribe(events.WINDOW_EDIT, self.onEdit)
        pub.subscribe(events.CONSOLE_UPDATE, self.console.logOutput)
        pub.subscribe(events.EXECUTION_COMPLETE, self.onComplete)
        pub.subscribe(events.PROGRESS_UPDATE, self.footer.updateProgressBar)
        pub.subscribe(events.TIME_UPDATE, self.footer.updateTimeRemaining)
        # Top level wx close event
        self.Bind(wx.EVT_CLOSE, self.onClose)

        if self.buildSpec['poll_external_updates']:
            self.fetchExternalUpdates()

        if self.buildSpec.get('auto_start', False):
            self.onStart()

    def applyConfiguration(self):
        self.SetTitle(self.buildSpec['program_name'])
        self.SetBackgroundColour(self.buildSpec.get('body_bg_color'))

    def onStart(self, *args, **kwarg):
        """
        Verify user input and kick off the client's program if valid
        """
        with transactUI(self):
            config = self.navbar.getActiveConfig()
            config.resetErrors()
            if config.isValid():
                if self.buildSpec['clear_before_run']:
                    self.console.clear()
                self.clientRunner.run(self.buildCliString())
                self.showConsole()
            else:
                config.displayErrors()
                self.Layout()
        
    def onEdit(self):
        """Return the user to the settings screen for further editing"""
        with transactUI(self):
            if self.buildSpec['poll_external_updates']:
                self.fetchExternalUpdates()
            self.showSettings()


    def buildCliString(self):
        """
        Collect all of the required information from the config screen and
        build a CLI string which can be used to invoke the client program
        """
        config = self.navbar.getActiveConfig()
        group = self.buildSpec['widgets'][self.navbar.getSelectedGroup()]
        positional = config.getPositionalArgs()
        optional = config.getOptionalArgs()
        return cli.buildCliString(
            self.buildSpec['target'],
            group['command'],
            positional,
            optional,
            suppress_gooey_flag=self.buildSpec['suppress_gooey_flag']
        )


    def onComplete(self, *args, **kwargs):
        """
        Display the appropriate screen based on the success/fail of the
        host program
        """
        with transactUI(self):
            if self.clientRunner.was_success():
                if self.buildSpec.get('return_to_config', False):
                    self.showSettings()
                else:
                    self.showSuccess()
                    if self.buildSpec.get('show_success_modal', True):
                        wx.CallAfter(modals.showSuccess)
            else:
                if self.clientRunner.wasForcefullyStopped:
                    self.showForceStopped()
                else:
                    self.showError()
                    if self.buildSpec.get('show_failure_modal'):
                        wx.CallAfter(modals.showFailure)

    def onCancel(self):
        """Close the program after confirming

        We treat the behavior of the "cancel" button slightly
        differently than the general window close X button only
        because this is 'part of' the form.
        """
        if modals.confirmExit():
            self.onClose()


    def onStopExecution(self):
        """Displays a scary message and then force-quits the executing
        client code if the user accepts"""
        if self.shouldStopExecution():
            self.clientRunner.stop()


    def onClose(self, *args, **kwargs):
        """Stop any actively running client program, cleanup the top
        level WxFrame and shutdown the current process"""
        # issue #592 - we need to run the same onStopExecution machinery
        # when the exit button is clicked to ensure everything is cleaned
        # up correctly.
        if self.clientRunner.running():
            if self.shouldStopExecution():
                self.clientRunner.stop()
                self.destroyGooey()
        else:
            self.destroyGooey()


    def shouldStopExecution(self):
        return not self.buildSpec['show_stop_warning'] or modals.confirmForceStop()


    def destroyGooey(self):
        self.Destroy()
        sys.exit()

    def fetchExternalUpdates(self):
        """
        !Experimental!
        Calls out to the client code requesting seed values to use in the UI
        !Experimental!
        """
        seeds = seeder.fetchDynamicProperties(
            self.buildSpec['target'],
            self.buildSpec['encoding']
        )
        for config in self.configs:
            config.seedUI(seeds)

    def layoutComponent(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.header, 0, wx.EXPAND)
        sizer.Add(wx_util.horizontal_rule(self), 0, wx.EXPAND)

        sizer.Add(self.navbar, 1, wx.EXPAND)
        sizer.Add(self.console, 1, wx.EXPAND)
        sizer.Add(wx_util.horizontal_rule(self), 0, wx.EXPAND)
        sizer.Add(self.footer, 0, wx.EXPAND)
        self.SetMinSize((400, 300))
        self.SetSize(self.buildSpec['default_size'])
        self.SetSizer(sizer)
        self.console.Hide()
        self.Layout()
        if self.buildSpec.get('fullscreen', True):
            self.ShowFullScreen(True)
        # Program Icon (Windows)
        icon = wx.Icon(self.buildSpec['images']['programIcon'], wx.BITMAP_TYPE_PNG)
        self.SetIcon(icon)
        if sys.platform != 'win32':
            # OSX needs to have its taskbar icon explicitly set
            # bizarrely, wx requires the TaskBarIcon to be attached to the Frame
            # as instance data (self.). Otherwise, it will not render correctly.
            self.taskbarIcon = TaskBarIcon(iconType=wx.adv.TBI_DOCK)
            self.taskbarIcon.SetIcon(icon)



    def buildNavigation(self):
        """
        Chooses the appropriate layout navigation component based on user prefs
        """
        if self.buildSpec['navigation'] == constants.TABBED:
            navigation = Tabbar(self, self.buildSpec, self.configs)
        else:
            navigation = Sidebar(self, self.buildSpec, self.configs)
            if self.buildSpec['navigation'] == constants.HIDDEN:
                navigation.Hide()
        return navigation


    def buildConfigPanels(self, parent):
        page_class = TabbedConfigPage if self.buildSpec['tabbed_groups'] else ConfigPage

        return [page_class(parent, widgets, self.buildSpec)
                for widgets in self.buildSpec['widgets'].values()]


    def showSettings(self):
        self.navbar.Show(True)
        self.console.Show(False)
        self.header.setImage('settings_img')
        self.header.setTitle(_("settings_title"))
        self.header.setSubtitle(self.buildSpec['program_description'])
        self.footer.showButtons('cancel_button', 'start_button')
        self.footer.progress_bar.Show(False)
        self.footer.time_remaining_text.Show(False)


    def showConsole(self):
        self.navbar.Show(False)
        self.console.Show(True)
        self.header.setImage('running_img')
        self.header.setTitle(_("running_title"))
        self.header.setSubtitle(_('running_msg'))
        self.footer.showButtons('stop_button')
        self.footer.progress_bar.Show(True)
        self.footer.time_remaining_text.Show(False)
        if self.buildSpec.get('timing_options')['show_time_remaining']:
            self.timer.start()
            self.footer.time_remaining_text.Show(True)
        if not self.buildSpec['progress_regex']:
            self.footer.progress_bar.Pulse()


    def showComplete(self):
        self.navbar.Show(False)
        self.console.Show(True)
        buttons = (['edit_button', 'restart_button', 'close_button']
                   if self.buildSpec.get('show_restart_button', True)
                   else ['edit_button', 'close_button'])
        self.footer.showButtons(*buttons)
        self.footer.progress_bar.Show(False)
        if self.buildSpec.get('timing_options')['show_time_remaining']:
            self.timer.stop()
        self.footer.time_remaining_text.Show(True)
        if self.buildSpec.get('timing_options')['hide_time_remaining_on_complete']:
            self.footer.time_remaining_text.Show(False)



    def showSuccess(self):
        self.showComplete()
        self.header.setImage('check_mark')
        self.header.setTitle(_('finished_title'))
        self.header.setSubtitle(_('finished_msg'))
        self.Layout()


    def showError(self):
        self.showComplete()
        self.header.setImage('error_symbol')
        self.header.setTitle(_('finished_title'))
        self.header.setSubtitle(_('finished_error'))


    def showForceStopped(self):
        self.showComplete()
        if self.buildSpec.get('force_stop_is_error', True):
            self.showError()
        else:
            self.showSuccess()
        self.header.setSubtitle(_('finished_forced_quit'))


