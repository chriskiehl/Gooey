from contextlib import contextmanager

from gooey.gui.components.widgets.bases import TextContainer
import wx  # type: ignore

from gooey.gui import formatters
from gooey.gui.lang.i18n import _
from gooey.python_bindings import types as t
from gooey.python_bindings.types import FormField


class Dropdown(TextContainer):
    _gooey_options = {
        'placeholder': str,
        'readonly': bool,
        'enable_autocomplete': bool
    }
    def getWidget(self, parent, *args, **options):
        default = _('select_option')
        return wx.ComboBox(
            parent=parent,
            id=-1,
            # str conversion allows using stringyfiable values in addition to pure strings
            value=str(default),
            choices=[str(default)] + [str(choice) for choice in self._meta['choices']],
            style=wx.CB_DROPDOWN)

    def setOptions(self, options):
        with self.retainSelection():
            self.widget.Clear()
            self.widget.SetItems([_('select_option')] + options)

    def setValue(self, value):
        ## +1 to offset the default placeholder value
        index = self._meta['choices'].index(value) + 1
        self.widget.SetSelection(index)

    def getWidgetValue(self):
        value = self.widget.GetValue()
        # filter out the extra default option that's
        # appended during creation
        if value == _('select_option'):
            return None
        return value

    def formatOutput(self, metadata, value):
        return formatters.dropdown(metadata, value)


    def syncUiState(self, state: FormField):
        self.setOptions(state['choices'])  # type: ignore
        if state['selected'] is not None:  # type: ignore
            self.setValue(state['selected'])  # type: ignore
        self.error.SetLabel(state['error'] or '')
        self.error.Show(state['error'] is not None and state['error'] is not '')

    def getUiState(self) -> t.FormField:
        widget: wx.ComboBox = self.widget
        return t.Dropdown(
            id=self._id,
            type=self.widgetInfo['type'],
            selected=self.getWidgetValue(),
            choices=widget.GetStrings(),
            error=self.error.GetLabel() or None,
            enabled=self.IsEnabled(),
            visible=self.IsShown()
        )

    @contextmanager
    def retainSelection(self):
        """"
        Retains the selected dropdown option (when possible)
        across mutations due to dynamic updates.
        """
        prevSelection = self.widget.GetSelection()
        prevValue = self.widget.GetValue()
        try:
            yield
        finally:
            current_at_index = self.widget.GetString(prevSelection)
            if prevValue == current_at_index:
                self.widget.SetSelection(prevSelection)
            else:
                self.widget.SetSelection(0)
