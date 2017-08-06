from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtWidgets import QStackedWidget

import gooey.gui.components.widgets as gooey_widgets
from gooey.gui.processor import ProcessController
from gooey.gui.components.config_panel import ConfigPanel
from gooey.gui.components.console_panel import ConsolePanel
from gooey.gui.components.footer import Footer
from gooey.gui.components.header import Header
from gooey.gui.containers.layouts import StockLayout, SplitLayout, WithTabs
from gooey.gui import image_repository
from gooey.gui.commandline import build_cmd_str
from gooey.gui.components.sidebar import Sidebar
from gooey.gui.util import isRequired, isOptional, belongsTo, flatten, forEvent
from gooey.gui.util import nestedget

from gooey.gui.lang.i18n import _


class MainWindow(QMainWindow):
    # todo: proper controller

    def __init__(self, state, parent=None):
        super(MainWindow, self).__init__(parent)

        self.clientRunner = ProcessController('', '')

        self._state = state

        self.setWindowTitle(self._state['program_name'])
        self.resize(*self._state['default_size'])

        self.header = Header(self)
        self.footer = Footer(self)

        self.sidebar = Sidebar(self, state['groups'].keys())
        self.qwidgets = self.constructWidgets(state)
        self.configPanels = self.buildConfigStack(state, self.qwidgets)
        self.configPanels.setCurrentIndex(0)

        self.configScreen = SplitLayout(
            self,
            self.sidebar,
            self.configPanels
        )

        self.console = ConsolePanel(self)

        self.bodyStack = QStackedWidget(self)
        self.bodyStack.addWidget(self.configScreen)
        self.bodyStack.addWidget(self.console)

        self.container = StockLayout(self.header, self.bodyStack, self.footer)
        self.setCentralWidget(self.container)

        self._state.map(nestedget(['gooey_state', 'title'])).subscribe(self.header.setTitle)
        self._state.map(nestedget(['gooey_state', 'subtitle'])).subscribe(self.header.setSubtitle)
        self._state.map(nestedget(['gooey_state', 'icon'])).subscribe(self.header.setIcon)
        self._state.map(nestedget(['gooey_state', 'window'])).subscribe(self.setActiveBody)
        self._state.map(nestedget(['gooey_state', 'buttonGroup'])).subscribe(self.footer.setVisibleGroup)
        self.footer.buttons.filter(forEvent('START')).subscribe(self.handleStart)
        self.footer.buttons.filter(forEvent('STOP')).subscribe(self.handleStop)
        self.footer.buttons.filter(forEvent('CLOSE')).subscribe(self.handleClose)
        self.footer.buttons.filter(forEvent('RESTART')).subscribe(self.handleStart)
        self.footer.buttons.filter(forEvent('QUIT')).subscribe(self.handleClose)
        self.footer.buttons.filter(forEvent('EDIT')).subscribe(self.handleEdit)
        self.sidebar.value.subscribe(self.handleSidebarChange)
        for widget in flatten(self.qwidgets):
            widget.value.subscribe(self.handleWidgetUpdate)

        # Hide the sidebar if we're not in a sub-parser mode
        if len(state['groups']) == 1:
            self.configScreen.hideLeft()


    def setActiveBody(self, index):
        self.bodyStack.setCurrentIndex(index)


    def constructWidgets(self, state):
        output = []
        groups, widgets = state['groups'].keys(), state['widgets']
        for group in groups:
            groupedWidgets = list(filter(belongsTo(group), widgets.values()))
            required = list(filter(isRequired, groupedWidgets))
            optional = list(filter(isOptional, groupedWidgets))

            rout = []
            oout = []
            for widget in required:
                widget_class = getattr(gooey_widgets, widget['type'])
                rout.append(widget_class(self, widget))
            for widget in optional:
                widget_class = getattr(gooey_widgets, widget['type'])
                oout.append(widget_class(self, widget))

            output.append((rout, oout))
        return output


    def buildConfigStack(self, state, qwidgets):
        stack = QStackedWidget(self)
        for required, optional in qwidgets:
            stack.addWidget(ConfigPanel(state, required, optional))
        return stack


    def handleSidebarChange(self, action):
        self._state['activeGroup'] = action['group']
        self.configPanels.setCurrentIndex(action['value'])


    def handleWidgetUpdate(self, action):
        self._state['widgets'][action['id']]['cmd'] = action['cmd']


    def handleStart(self, action):
        activeGroup = self._state['activeGroup']
        activeWidgets = list(filter(belongsTo(activeGroup), self._state['widgets'].values()))
        # if not self.hasRequiredArgs(activeWidgets):
        #     self.launchDialog(
        #         'warning',
        #         _('error_title'),
        #         _('error_required_fields')
        #     )
        #     return

        command = build_cmd_str(
            self._state,
            list(filter(belongsTo(activeGroup),
            self._state['widgets'].values()))
        )

        self.do2()

        self.clientRunner.run(command)
        self.clientRunner.subject.subscribe(
            on_next=self.doThing,
            on_error=lambda *args, **kwargs: print('ERROR!', args, kwargs)
        )


    def doThing(self, event):
        if event.get('completed'):
            self.doOtherThing()
        else:
            self.console.writeLine(event.get('console_update').decode('utf-8'))


    def doOtherThing(self):
        if self.clientRunner.was_success():
            self.do3()
            QTimer().singleShot(0, self.successDialog)
        else:
            self.do4()
            QTimer().singleShot(0, self.runtimeErrorDialog)


    def hasRequiredArgs(self, widgets):
        # todo: basic type validation (e.g. 'must be number')
        required = list(filter(isRequired, widgets))
        return all(x.get('cmd') for x in required)



    def handleStop(self, action):
        if self.confirmStop():
            self.clientRunner.stop()


    def handleClose(self, action):
        self.close()


    def handleRestart(self, action):
        self.handleStart(action)


    def handleEdit(self, action):
        self.do1()

    def launchDialog(self, boxtype, title, body):
        def launchDialog():
            getattr(QMessageBox, boxtype)(
                self, title, body, QMessageBox.Ok, QMessageBox.NoButton
            )
        QTimer().singleShot(0, launchDialog)


    def successDialog(self):
        self.launchDialog(
            'information', _('execution_finished'), _('success_message')
        )


    def runtimeErrorDialog(self):
        self.launchDialog(
            'critical', _('error_title'), _('uh_oh')
        )


    def launchConfirmDialog(self, title, body):
        result = QMessageBox.question(
            self, title, body, QMessageBox.Ok, QMessageBox.Cancel
        )
        return result == QMessageBox.Ok


    def confirmStop(self):
        return self.launchConfirmDialog(
            _('stop_task'),
            _('sure_you_want_to_stop')
        )


    def do1(self):
        self._state['gooey_state'] = {
            'icon': image_repository.config_icon,
            'title': _('settings_title'),
            'subtitle': self._state['program_description'],
            'window': 0,
            'buttonGroup': 0
        }

    def do2(self):
        self._state['gooey_state'] = {
            'icon': image_repository.running_icon,
            'title': _('running_title'),
            'subtitle': _('running_msg'),
            'window': 1,
            'buttonGroup': 1
        }

    def do3(self):
        self._state['gooey_state'] = {
            'icon': image_repository.success_icon,
            'title': _('finished_title'),
            'subtitle': _('finished_msg'),
            'window': 1,
            'buttonGroup': 2
        }

    def do4(self):
        self._state['gooey_state'] = {
            'icon': image_repository.error_icon,
            'title':  _('finished_title'),
            'subtitle': _('finished_error'),
            'window': 1,
            'buttonGroup': 2
        }

