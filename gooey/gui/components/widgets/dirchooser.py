from PyQt5.QtWidgets import QFileDialog

from gooey.gui.components.widgets.chooser import Chooser


class DirectoryChooser(Chooser):
    launchDialog = QFileDialog.getExistingDirectory

    def processResult(self, result):
        return result

