from functools import partial
from itertools import groupby
from operator import itemgetter

from PyQt5.QtWidgets import QHBoxLayout, \
    QStackedWidget, QProgressBar
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QWidget
from rx.subjects.subject import Subject

from gooey.gui.lang.i18n import _



class Footer(QWidget):

    def __init__(self, parent, *args, **kwargs):
        super(Footer, self).__init__(parent, *args, **kwargs)
        self.buttons = Subject()

        self.progressBar = QProgressBar()
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(0)

        self.spacer = QWidget()
        self.buttonStack = self.createButtonStack()
        self.layoutComponent()

    def createButtonStack(self):
        def dispatch(action):
            self.buttons.on_next({'type': action})

        buttonStack = QStackedWidget()
        groups = groupby(self.buttonDetails(), itemgetter('group'))
        for group, details in groups:
            q = QWidget()
            layout = QHBoxLayout()
            for item in details:
                appliedDispatch = partial(dispatch, item['type'])
                button = QPushButton(item['label'])
                button.clicked.connect(appliedDispatch)
                layout.addWidget(button)
            q.setLayout(layout)
            buttonStack.addWidget(q)
        return buttonStack

    def layoutComponent(self):
        layout = QHBoxLayout()
        layout.addWidget(self.progressBar, stretch=1)
        layout.addWidget(self.spacer, stretch=1)
        layout.addWidget(self.buttonStack)
        self.progressBar.setVisible(False)
        self.spacer.setVisible(True)

        self.setLayout(layout)
        self.setMinimumHeight(60)
        self.setMaximumHeight(60)

    def setVisibleGroup(self, group):
        self.buttonStack.setCurrentIndex(group)

    def buttonDetails(self):
        return [
            {'label': _('cancel'), 'type': 'CLOSE', 'group': 'config'},
            {'label': _('start'), 'type': 'START', 'group': 'config'},
            {'label': _('stop'), 'type': 'STOP', 'group': 'running'},
            {'label': _('edit'), 'type': 'EDIT', 'group': 'complete'},
            {'label': _('restart'), 'type': 'RESTART', 'group': 'complete'},
            {'label': _('close'), 'type': 'QUIT', 'group': 'complete'},
        ]
