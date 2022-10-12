import wx  # type: ignore

from gooey.gui import formatters
from gooey.gui.components.widgets.bases import TextContainer
from gooey.python_bindings import types as t

class IntegerField(TextContainer):
    """
    An integer input field
    """
    widget_class = wx.SpinCtrl
    def getWidget(self, *args, **options):
        widget = self.widget_class(self,
                             value='',
                             min=self._options.get('min', 0),
                             max=self._options.get('max', 100))
        return widget

    def getWidgetValue(self):
        return self.widget.GetValue()

    def setValue(self, value):
        self.widget.SetValue(int(value))

    def formatOutput(self, metatdata, value):
        # casting to string so that the generic formatter
        # doesn't treat 0 as false/None
        return formatters.general(metatdata, str(value))

    def getUiState(self) -> t.FormField:
        widget: wx.SpinCtrl = self.widget
        return t.IntegerField(
            id=self._id,
            type=self.widgetInfo['type'],
            value=self.getWidgetValue(),
            min=widget.GetMin(),
            max=widget.GetMax(),
            error=self.error.GetLabel() or None,
            enabled=self.IsEnabled(),
            visible=self.IsShown()
        )

class DecimalField(IntegerField):
    """
    A decimal input field
    """
    widget_class = wx.SpinCtrlDouble

    def getWidget(self, *args, **options):
        widget = self.widget_class(self,
                             value='',
                             min=self._options.get('min', 0),
                             max=self._options.get('max', 100),
                             inc=self._options.get('increment', 0.01))
        widget.SetDigits(self._options.get('precision', widget.GetDigits()))
        return widget


    def setValue(self, value):
        self.widget.SetValue(value)

    def getUiState(self) -> t.FormField:
        widget: wx.SpinCtrlDouble = self.widget
        return t.IntegerField(
            id=self._id,
            type=self.widgetInfo['type'],
            value=self.getWidgetValue(),
            min=widget.GetMin(),
            max=widget.GetMax(),
            error=self.error.GetLabel() or None,
            enabled=self.IsEnabled(),
            visible=self.IsShown()
        )
