from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton

from gooey.gui.components.widgets.textfield import TextField
from gooey.gui import formatters


# TODO: unify all of the return types Qt throws out
# TODO: of the various Dialogs
class Chooser(TextField):
    widget_class = QLineEdit
    launchDialog = None

    def getSublayout(self, *args, **kwargs):
        self.button = QPushButton('Browse')
        self.button.clicked.connect(self.spawnDialog)

        layout = QHBoxLayout()
        layout.addWidget(self.widget, stretch=1)
        layout.addWidget(self.button)
        return layout

    def spawnDialog(self, *args, **kwargs):
        if not callable(self.launchDialog):
            raise AssertionError(
                'Chooser subclasses must provide QFileDialog callable '
                'to launchDialog property (.e.g '
                '`launchDialog = QFileDialog.getOpenFileName`'
            )
        result = self.launchDialog(parent=self)
        if result:
            self.setValue(self.processResult(result))

    def processResult(self, result):
        return result[0]


    def formatOutput(self, metatdata, value):
        return formatters.general(metatdata, value)
