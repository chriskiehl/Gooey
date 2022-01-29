import sys
from json import JSONDecodeError

import six
import wx  # type: ignore

from gooey import Events
from gooey.gui import events
from gooey.gui import host
from gooey.gui import state as s
from gooey.gui.application.components import RHeader, ProgressSpinner, ErrorWarning, RTabbedLayout, \
    RSidebar, RFooter
from gooey.gui.components import modals
from gooey.gui.components.config import ConfigPage
from gooey.gui.components.config import TabbedConfigPage
from gooey.gui.components.console import Console
from gooey.gui.components.menubar import MenuBar
from gooey.gui.lang.i18n import _
from gooey.gui.processor import ProcessController
from gooey.gui.pubsub import pub
from gooey.gui.state import FullGooeyState
from gooey.gui.state import initial_state, ProgressEvent, TimingEvent
from gooey.gui.util.wx_util import transactUI, callafter
from gooey.python_bindings import constants
from gooey.python_bindings.dynamics import unexpected_exit_explanations, \
    deserialize_failure_explanations
from gooey.python_bindings.types import PublicGooeyState
from gooey.python_bindings.types import Try
from gooey.util.functional import assoc
from gooey.gui.util.time import Timing
from rewx import components as c  # type: ignore
from rewx import wsx  # type: ignore
from rewx.core import Component, Ref  # type: ignore


class RGooey(Component):
    """
    Main Application container for Gooey.

    State Management
    ----------------

    Pending further refactor, state is tracked in two places:
    1. On this instance (React style)
    2. In the WX Form Elements themselves[0]

    As needed, these two states are merged to form the `FullGooeyState`, which
    is the canonical state object against which all logic runs.


    Dynamic Updates
    ---------------




    [0] this is legacy and will (eventually) be refactored away

    """
    def __init__(self, props):
        super().__init__(props)
        self.frameRef = Ref()
        self.consoleRef = Ref()
        self.configRef = Ref()

        self.buildSpec = props
        self.state = initial_state(props)
        self.headerprops = lambda state: {
            'background_color': self.buildSpec['header_bg_color'],
            'title': state['title'],
            'show_title': state['header_show_title'],
            'subtitle': state['subtitle'],
            'show_subtitle': state['header_show_subtitle'],
            'flag': wx.EXPAND,
            'height': self.buildSpec['header_height'],
            'image_uri': state['image'],
            'image_size': (six.MAXSIZE, self.buildSpec['header_height'] - 10)}

        self.fprops = lambda state: {
            'buttons': state['buttons'],
            'progress': state['progress'],
            'timing': state['timing'],
            'bg_color': self.buildSpec['footer_bg_color'],
            'flag': wx.EXPAND,
        }
        self.clientRunner = ProcessController.of(self.buildSpec)
        self.timer = None


    def component_did_mount(self):
        pub.subscribe(events.WINDOW_START, self.onStart)
        pub.subscribe(events.WINDOW_RESTART, self.onStart)
        pub.subscribe(events.WINDOW_STOP, self.handleInterrupt)
        pub.subscribe(events.WINDOW_CLOSE, self.handleClose)
        pub.subscribe(events.WINDOW_CANCEL, self.handleCancel)
        pub.subscribe(events.WINDOW_EDIT, self.handleEdit)
        pub.subscribe(events.CONSOLE_UPDATE, self.consoleRef.instance.logOutput)
        pub.subscribe(events.EXECUTION_COMPLETE, self.handleComplete)
        pub.subscribe(events.PROGRESS_UPDATE, self.updateProgressBar)
        pub.subscribe(events.TIME_UPDATE, self.updateTime)
        # # Top level wx close event
        frame: wx.Frame = self.frameRef.instance
        frame.Bind(wx.EVT_CLOSE, self.handleClose)
        frame.SetMenuBar(MenuBar(self.buildSpec))
        self.timer = Timing(frame)

        if self.state['fullscreen']:
            frame.ShowFullScreen(True)

        if self.state['show_preview_warning'] and not 'unittest' in sys.modules.keys():
            wx.MessageDialog(None, caption='YOU CAN DISABLE THIS MESSAGE',
                             message="""
                This is a preview build of 1.2.0! There may be instability or 
                broken functionality. If you encounter any issues, please open an issue 
                here: https://github.com/chriskiehl/Gooey/issues 
                
                The current stable version is 1.0.8. 
                
                NOTE! You can disable this message by setting `show_preview_warning` to False. 
                
                e.g. 
                `@Gooey(show_preview_warning=False)`
                """).ShowModal()

    def getActiveConfig(self):
        return [item
                for child in self.configRef.instance.Children
                # we descend down another level of children  to account
                # for Notebook layouts (which have wrapper objects)
                for item in [child] + list(child.Children)
                if isinstance(item, ConfigPage)
                or isinstance(item, TabbedConfigPage)][self.state['activeSelection']]

    def getActiveFormState(self):
        """
        This boiler-plate and manual interrogation of the UIs
        state is required until we finish porting the Config Form
        over to rewx (which is a battle left for another day given
        its complexity)
        """
        return self.getActiveConfig().getFormState()


    def fullState(self):
        """
        Re: final porting is a to do. For now we merge the UI
        state into the main tracked state.
        """
        formState = self.getActiveFormState()
        return s.combine(self.state, self.props, formState)


    def onStart(self, *args, **kwargs):
        """
        Dispatches the start behavior.
        """
        if Events.VALIDATE_FORM in self.state['use_events']:
            self.runAsyncValidation()
        else:
            self.startRun()


    def startRun(self):
        """
        Kicks off a run by invoking the host's code
        and pumping its stdout to Gooey's Console window.
        """
        state = self.fullState()
        if state['clear_before_run']:
            self.consoleRef.instance.Clear()
        self.set_state(s.consoleScreen(_, state))
        self.clientRunner.run(s.buildInvocationCmd(state))
        self.timer.start()
        self.frameRef.instance.Layout()
        for child in self.frameRef.instance.Children:
            child.Layout()


    def syncExternalState(self, state: FullGooeyState):
        """
        Sync the UI's state to what the host program has requested.
        """
        self.getActiveConfig().syncFormState(s.activeFormState(state))
        self.frameRef.instance.Layout()
        for child in self.frameRef.instance.Children:
            child.Layout()


    def handleInterrupt(self, *args, **kwargs):
        if self.shouldStopExecution():
            self.clientRunner.stop()

    def handleComplete(self, *args, **kwargs):
        self.timer.stop()
        if self.clientRunner.was_success():
            self.handleSuccessfulRun()
            if Events.ON_SUCCESS in self.state['use_events']:
                self.runAsyncExternalOnCompleteHandler(was_success=True)
        else:
            self.handleErrantRun()
            if Events.ON_ERROR in self.state['use_events']:
                self.runAsyncExternalOnCompleteHandler(was_success=False)

    def handleSuccessfulRun(self):
        if self.state['return_to_config']:
            self.set_state(s.editScreen(_, self.state))
        else:
            self.set_state(s.successScreen(_, self.state))
            if self.state['show_success_modal']:
                wx.CallAfter(modals.showSuccess)


    def handleErrantRun(self):
        if self.clientRunner.wasForcefullyStopped:
            self.set_state(s.interruptedScreen(_, self.state))
        else:
            self.set_state(s.errorScreen(_, self.state))
            if self.state['show_failure_modal']:
                wx.CallAfter(modals.showFailure)


    def successScreen(self):
        strings = {'title': _('finished_title'), 'subtitle': _('finished_msg')}
        self.set_state(s.success(self.state, strings, self.buildSpec))


    def handleEdit(self, *args, **kwargs):
        self.set_state(s.editScreen(_, self.state))

    def handleCancel(self, *args, **kwargs):
        if modals.confirmExit():
            self.handleClose()

    def handleClose(self, *args, **kwargs):
        """Stop any actively running client program, cleanup the top
        level WxFrame and shutdown the current process"""
        # issue #592 - we need to run the same onStopExecution machinery
        # when the exit button is clicked to ensure everything is cleaned
        # up correctly.
        frame: wx.Frame = self.frameRef.instance
        if self.clientRunner.running():
            if self.shouldStopExecution():
                self.clientRunner.stop()
                frame.Destroy()
                # TODO: NOT exiting here would allow
                # spawing the gooey to input params then
                # returning control to the CLI
                sys.exit()
        else:
            frame.Destroy()
            sys.exit()

    def shouldStopExecution(self):
        return not self.state['show_stop_warning'] or modals.confirmForceStop()

    def updateProgressBar(self, *args, progress=None):
        self.set_state(s.updateProgress(self.state, ProgressEvent(progress=progress)))

    def updateTime(self, *args, elapsed_time=None, estimatedRemaining=None, **kwargs):
        event = TimingEvent(elapsed_time=elapsed_time, estimatedRemaining=estimatedRemaining)
        self.set_state(s.updateTime(self.state, event))

    def handleSelectAction(self, event):
        self.set_state(assoc(self.state, 'activeSelection', event.Selection))


    def runAsyncValidation(self):
        def handleHostResponse(hostState: PublicGooeyState):
            self.set_state(s.finishUpdate(self.state))
            currentState = self.fullState()
            self.syncExternalState(s.mergeExternalState(currentState, hostState))
            if not s.has_errors(self.fullState()):
                self.startRun()
            else:
                self.set_state(s.editScreen(_, s.show_alert(self.fullState())))

        def onComplete(result: Try[PublicGooeyState]):
            result.onSuccess(handleHostResponse)
            result.onError(self.handleHostError)

        self.set_state(s.beginUpdate(self.state))
        fullState = self.fullState()
        host.communicateFormValidation(fullState, callafter(onComplete))


    def runAsyncExternalOnCompleteHandler(self, was_success):
        def handleHostResponse(hostState):
            if hostState:
                self.syncExternalState(s.mergeExternalState(self.fullState(), hostState))

        def onComplete(result: Try[PublicGooeyState]):
            result.onError(self.handleHostError)
            result.onSuccess(handleHostResponse)

        if was_success:
            host.communicateSuccessState(self.fullState(), callafter(onComplete))
        else:
            host.communicateErrorState(self.fullState(), callafter(onComplete))


    def handleHostError(self, ex):
        """
        All async errors get pumped here where we dump out the
        error and they hopefully provide a lot of helpful debugging info
        for the user.
        """
        try:
            self.set_state(s.errorScreen(_, self.state))
            self.consoleRef.instance.appendText(str(ex))
            self.consoleRef.instance.appendText(str(getattr(ex, 'output', '')))
            self.consoleRef.instance.appendText(str(getattr(ex, 'stderr', '')))
            raise ex
        except JSONDecodeError as e:
            self.consoleRef.instance.appendText(deserialize_failure_explanations)
        except Exception as e:
            self.consoleRef.instance.appendText(unexpected_exit_explanations)
        finally:
            self.set_state({**self.state, 'fetchingUpdate': False})


    def render(self):
        return wsx(
            [c.Frame, {'title': self.buildSpec['program_name'],
                       'background_color': self.buildSpec['body_bg_color'],
                       'double_buffered': True,
                       'min_size': (400, 300),
                       'icon_uri': self.state['images']['programIcon'],
                       'size': self.buildSpec['default_size'],
                       'ref': self.frameRef},
             [c.Block, {'orient': wx.VERTICAL},
              [RHeader, self.headerprops(self.state)],
              [c.StaticLine, {'style': wx.LI_HORIZONTAL, 'flag': wx.EXPAND}],
              [ProgressSpinner, {'show': self.state['fetchingUpdate']}],
              [ErrorWarning, {'show': self.state['show_error_alert'],
                              'uri': self.state['images']['errorIcon']}],
              [Console, {**self.buildSpec,
                         'flag': wx.EXPAND,
                         'proportion': 1,
                         'show': self.state['screen'] == 'CONSOLE',
                         'ref': self.consoleRef}],
              [RTabbedLayout if self.buildSpec['navigation'] == constants.TABBED else RSidebar,
               {'bg_color': self.buildSpec['sidebar_bg_color'],
                'label': 'Some Action!',
                'tabbed_groups': self.buildSpec['tabbed_groups'],
                'show_sidebar': self.state['show_sidebar'],
                'ref': self.configRef,
                'show': self.state['screen'] == 'FORM',
                'activeSelection': self.state['activeSelection'],
                'options': list(self.buildSpec['widgets'].keys()),
                'on_change': self.handleSelectAction,
                'config': self.buildSpec['widgets'],
                'flag': wx.EXPAND,
                'proportion': 1}],
              [c.StaticLine, {'style': wx.LI_HORIZONTAL, 'flag': wx.EXPAND}],
              [RFooter, self.fprops(self.state)]]]
        )




