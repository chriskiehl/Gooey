import wx  # type: ignore

from gooey.gui import formatters
from gooey.gui.components.widgets.bases import TextContainer
from gooey.gui.lang.i18n import _
from gooey.gui.util import wx_util
from gooey.python_bindings import types as t


class CheckBox(TextContainer):

    widget_class = wx.CheckBox

    def arrange(self, *args, **kwargs):
        wx_util.make_bold(self.label)
        wx_util.withColor(self.label, self._options['label_color'])
        wx_util.withColor(self.help_text, self._options['help_color'])
        wx_util.withColor(self.error, self._options['error_color'])
        self.error.Hide()

        self.help_text.SetMinSize((0,-1))

        layout = wx.BoxSizer(wx.VERTICAL)
        if self._options.get('show_label', True):
            layout.Add(self.label, 0, wx.EXPAND)
        else:
            self.label.Show(False)
            layout.AddStretchSpacer(1)

        layout.AddSpacer(2)
        if self.help_text:
            hsizer = wx.BoxSizer(wx.HORIZONTAL)
            hsizer.Add(self.widget, 0)
            hsizer.Add(self.help_text, 1)
            layout.Add(hsizer, 1, wx.EXPAND)
            layout.AddSpacer(2)
        else:
            layout.Add(self.widget, 0, wx.EXPAND)
            layout.AddStretchSpacer(1)
        return layout


    def setValue(self, value):
        self.widget.SetValue(value)

    def getWidgetValue(self):
        return self.widget.GetValue()


    def formatOutput(self, metatdata, value):
        return formatters.checkbox(metatdata, value)


    def hideInput(self):
        self.widget.Hide()


    def getUiState(self) -> t.FormField:
        return t.Checkbox(
            id=self._id,
            type='Checkbox',
            checked=self.widget.GetValue(),
            error=self.error.GetLabel() or None,  # type: ignore
            enabled=self.IsEnabled(),
            visible=self.IsShown()
        )

    def syncUiState(self, state: t.Checkbox):  # type: ignore
        checkbox: wx.CheckBox = self.widget
        checkbox.SetValue(state['checked'])
        checkbox.Enable(state['enabled'])
        self.Show(state['visible'])
        self.error.SetLabel(state['error'] or '')
        self.error.Show(state['error'] is not None and state['error'] != '')





class BlockCheckbox(CheckBox):
    """
    A block style layout which places the help text in the normal
    location rather than inline next to the checkbox. A replacement label
    called `block_label` is shown next to the checkbox control.

         +-----------------+
         |label            |
         |help_text        |
         |[ ] block_label  |
         +-----------------+
    This option tends to look better when there is a large amount of
    help text.
    """


    def arrange(self, *args, **kwargs):
        wx_util.make_bold(self.label)
        wx_util.withColor(self.label, self._options['label_color'])
        wx_util.withColor(self.help_text, self._options['help_color'])
        wx_util.withColor(self.error, self._options['error_color'])
        self.error.Hide()

        self.help_text.SetMinSize((0,-1))

        layout = wx.BoxSizer(wx.VERTICAL)

        if self._options.get('show_label', True):
            layout.Add(self.label, 0, wx.EXPAND)
        else:
            layout.AddStretchSpacer(1)

        layout.AddSpacer(2)
        if self.help_text and self._options.get('show_help', True):
            layout.Add(self.help_text, 1, wx.EXPAND)
            layout.AddSpacer(2)
        else:
            layout.AddStretchSpacer(1)

        layout.AddSpacer(2)

        block_label = self._options.get('checkbox_label', _('checkbox_label'))
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.widget, 0)
        hsizer.Add(wx.StaticText(self, label=block_label), 1)
        layout.Add(hsizer, 1, wx.EXPAND)
        layout.AddSpacer(2)

        return layout
