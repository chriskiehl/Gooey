from PyQt5.QtWidgets import QFileDialog

from gooey.gui.components.widgets.chooser import Chooser


class FileSaver(Chooser):
    launchDialog = QFileDialog.getSaveFileName
