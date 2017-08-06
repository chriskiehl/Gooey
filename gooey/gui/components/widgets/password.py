from PyQt5.QtWidgets import QLineEdit

from gooey.gui.components.widgets import TextField


class PasswordField(TextField):
    def __init__(self, *args, **kwargs):
        super(PasswordField, self).__init__(*args, **kwargs)
        self.widget.setEchoMode(QLineEdit.Password)
