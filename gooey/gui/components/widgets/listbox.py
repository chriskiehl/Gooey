import wx  # type: ignore

from gooey.gui import formatters
from gooey.gui.components.widgets.bases import TextContainer
from gooey.python_bindings import types as t


class Listbox(TextContainer):

    def getWidget(self, parent, *args, **options):
        height = self._options.get('height', 60)
        return wx.ListBox(
            parent=parent,
            choices=self._meta['choices'],
            size=(-1, height),
            style=wx.LB_MULTIPLE
        )

    def setOptions(self, options):
        self.widget.Clear()
        for option in options:
            self.widget.Append(option)

    def setValue(self, values):
        for string in values:
            self.widget.SetStringSelection(string)

    def getWidgetValue(self):
        return [self.widget.GetString(index)
                for index in self.widget.GetSelections()]

    def formatOutput(self, metadata, value):
        return formatters.listbox(metadata, value)

    def getUiState(self) -> t.FormField:
        widget: wx.ComboBox = self.widget
        return t.Listbox(
            id=self._id,
            type=self.widgetInfo['type'],
            selected=self.getWidgetValue(),
            choices=self._meta['choices'],
            error=self.error.GetLabel() or None,
            enabled=self.IsEnabled(),
            visible=self.IsShown()
        )

    def syncUiState(self, state: t.Listbox):  # type: ignore
        widget: wx.ComboBox = self.widget
        widget.Clear()
        widget.AppendItems(state.get('choices', []))
        for string in state['selected']:
            widget.SetStringSelection(string)
        self.error.SetLabel(state['error'] or '')
        self.error.Show(state['error'] is not None and state['error'] is not '')
