from gooey.gui.components.widgets.core.text_input import MultilineTextInput
from gooey.gui.components.widgets.textfield import TextField


class Textarea(TextField):
    widget_class = MultilineTextInput
