from gooey.gui.components.widgets.core.text_input import PasswordInput
from gooey.gui.components.widgets.textfield import TextField
from gooey.python_bindings import types as t

__ALL__ = ('PasswordField',)

class PasswordField(TextField):
    widget_class = PasswordInput  # type: ignore

    def __init__(self, *args, **kwargs):
        super(PasswordField, self).__init__(*args, **kwargs)

    def getUiState(self) -> t.FormField:  # type: ignore
        return t.PasswordField(**super().getUiState())  # type: ignore

