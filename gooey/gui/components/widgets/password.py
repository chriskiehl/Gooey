from gooey.gui.components.widgets.core.text_input import PasswordInput
from gooey.gui.components.widgets.textfield import TextField


__ALL__ = ('PasswordField',)

class PasswordField(TextField):
    widget_class = PasswordInput

    def __init__(self, *args, **kwargs):
        super(PasswordField, self).__init__(*args, **kwargs)

