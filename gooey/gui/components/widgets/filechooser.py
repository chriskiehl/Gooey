from PyQt5.QtWidgets import QFileDialog

from gooey.gui.components.widgets.chooser import Chooser


class FileChooser(Chooser):
    launchDialog = QFileDialog.getOpenFileName


