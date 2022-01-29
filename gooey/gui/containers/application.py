"""
Primary orchestration and control point for Gooey.
"""
import queue
import sys
import threading
from contextlib import contextmanager
from functools import wraps
from json import JSONDecodeError
from pprint import pprint
from subprocess import CalledProcessError
from threading import Thread, get_ident
from typing import Mapping, Dict, Type, Iterable

import six
import wx  # type: ignore

from gooey.gui.state import FullGooeyState
from gooey.python_bindings.types import PublicGooeyState
from rewx.widgets import set_basic_props

from gooey.gui.components.mouse import notifyMouseEvent
from gooey.gui.state import initial_state, present_time, form_page, ProgressEvent, TimingEvent
from gooey.gui import state as s
from gooey.gui.three_to_four import Constants
from rewx.core import Component, Ref, updatewx, patch
from typing_extensions import TypedDict

from rewx import wsx, render, create_element, mount, update
from rewx import components as c
from wx.adv import TaskBarIcon  # type: ignore
import signal

from gooey import Events
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
from gooey.python_bindings.types import Failure, Success, CommandDetails, Try
from gooey.util.functional import merge, associn, assoc
from gooey.gui.image_repository import loadImages
from gooey.gui import host


from threading import Lock

from gooey.util.functional import associnMany

lock = Lock()

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

        self.props = {
            'background_color': self.buildSpec['header_bg_color'],
            'title': self.buildSpec['program_name'],
            'subtitle': self.buildSpec['program_description'],
            'height': self.buildSpec['header_height'],
            'image_uri': self.buildSpec['images']['configIcon'],
            'image_size': (six.MAXSIZE, self.buildSpec['header_height'] - 10)}

        state = form_page(initial_state(self.buildSpec))

        self.fprops = {
            'buttons': state['buttons'],
            'progress': state['progress'],
            'timing': state['timing'],
            'bg_color': self.buildSpec['footer_bg_color']
        }

        # self.hhh = render(create_element(RHeader, self.props), self)
        # self.fff = render(create_element(RFooter, self.fprops), self)
        # patch(self.hhh, create_element(RHeader, {**self.props, 'image_uri': self.buildSpec['images']['runningIcon']}))
        self.layoutComponent()
        self.timer = Timing(self)

        self.clientRunner = ProcessController(
            self.buildSpec.get('progress_regex'),
            self.buildSpec.get('progress_expr'),
            self.buildSpec.get('hide_progress_msg'),
            self.buildSpec.get('encoding'),
            self.buildSpec.get('requires_shell'),
            self.buildSpec.get('shutdown_signal', signal.SIGTERM)
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
        # self.Bind(wx.EVT_CLOSE, self.onClose)

        # TODO: handle child focus for per-field level validation.
        # self.Bind(wx.EVT_CHILD_FOCUS, self.handleFocus)

        if self.buildSpec.get('auto_start', False):
            self.onStart()


    def applyConfiguration(self):
        self.SetTitle(self.buildSpec['program_name'])
        self.SetBackgroundColour(self.buildSpec.get('body_bg_color'))


    def onStart(self, *args, **kwarg):
        """
        Verify user input and kick off the client's program if valid
        """
        # navigates away from the button because a
        # disabled focused button still looks enabled.
        self.footer.cancel_button.Disable()
        self.footer.start_button.Disable()
        self.footer.start_button.Navigate()
        if Events.VALIDATE_FORM in self.buildSpec.get('use_events', []):
            # TODO: make this wx thread safe so that it can
            # actually run asynchronously
            Thread(target=self.onStartAsync).run()
        else:
            Thread(target=self.onStartAsync).run()

    def onStartAsync(self, *args, **kwargs):
        with transactUI(self):
            try:
                errors = self.validateForm().getOrThrow()
                if errors:  # TODO
                    config = self.navbar.getActiveConfig()
                    config.setErrors(errors)
                    self.Layout()
                    # TODO: account for tabbed layouts
                    # TODO: scroll the first error into view
                    # TODO: rather than just snapping to the top
                    self.configs[0].Scroll(0, 0)
                else:
                    if self.buildSpec['clear_before_run']:
                        self.console.clear()
                    self.clientRunner.run(self.buildCliString())
                    self.showConsole()
            except CalledProcessError as e:
                self.showError()
                self.console.appendText(str(e))
                self.console.appendText(
                    '\n\nThis failure happens when Gooey tries to invoke your '
                    'code for the VALIDATE_FORM event and receives an expected '
                    'error code in response.'
                )
                wx.CallAfter(modals.showFailure)
            except JSONDecodeError as e:
                self.showError()
                self.console.appendText(str(e))
                self.console.appendText(
                    '\n\nGooey was unable to parse the response to the VALIDATE_FORM event. '
                    'This can happen if you have additional logs to stdout beyond what Gooey '
                    'expects.'
                )
                wx.CallAfter(modals.showFailure)
            # for some reason, we have to delay the re-enabling of
            # the buttons by a few ms otherwise they pickup pending
            # events created while they were disabled. Trial and error
            # let to this solution.
            wx.CallLater(20, self.footer.start_button.Enable)
            wx.CallLater(20, self.footer.cancel_button.Enable)


    def onEdit(self):
        """Return the user to the settings screen for further editing"""
        with transactUI(self):
            for config in self.configs:
                config.resetErrors()
            self.showSettings()


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

    def buildCliString(self) -> str:
        """
        Collect all of the required information from the config screen and
        build a CLI string which can be used to invoke the client program
        """
        cmd = self.getCommandDetails()
        return cli.cliCmd(
            cmd.target,
            cmd.subcommand,
            cmd.positionals,
            cmd.optionals,
            suppress_gooey_flag=self.buildSpec['suppress_gooey_flag']
        )

    def validateForm(self) -> Try[Mapping[str, str]]:
        config = self.navbar.getActiveConfig()
        localErrors: Mapping[str, str] = config.getErrors()
        dynamicResult: Try[Mapping[str, str]] = self.fetchDynamicValidations()

        combineErrors = lambda m: merge(localErrors, m)
        return dynamicResult.map(combineErrors)


    def fetchDynamicValidations(self) -> Try[Mapping[str, str]]:
        # only run the dynamic validation if the user has
        # specifically subscribed to that event
        if Events.VALIDATE_FORM in self.buildSpec.get('use_events', []):
            cmd = self.getCommandDetails()
            return seeder.communicate(cli.formValidationCmd(
                cmd.target,
                cmd.subcommand,
                cmd.positionals,
                cmd.optionals
            ), self.buildSpec['encoding'])
        else:
            # shim response if nothing to do.
            return Success({})


    def getCommandDetails(self) -> CommandDetails:
        """
        Temporary helper for getting the state of the current Config.

        To be deprecated upon (the desperately needed) refactor.
        """
        config = self.navbar.getActiveConfig()
        group = self.buildSpec['widgets'][self.navbar.getSelectedGroup()]
        return CommandDetails(
            self.buildSpec['target'],
            group['command'],
            config.getPositionalValues(),
            config.getOptionalValues(),
        )


    def shouldStopExecution(self):
        return not self.buildSpec['show_stop_warning'] or modals.confirmForceStop()


    def destroyGooey(self):
        self.Destroy()
        sys.exit()

    def block(self, **kwargs):
        pass


    def layoutComponent(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        # sizer.Add(self.hhh, 0, wx.EXPAND)
        sizer.Add(self.header, 0, wx.EXPAND)
        sizer.Add(wx_util.horizontal_rule(self), 0, wx.EXPAND)

        sizer.Add(self.navbar, 1, wx.EXPAND)
        sizer.Add(self.console, 1, wx.EXPAND)
        sizer.Add(wx_util.horizontal_rule(self), 0, wx.EXPAND)
        # sizer.Add(self.fff, 0, wx.EXPAND)
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
        if not self.buildSpec.get('disable_progress_bar_animation', False):
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






