import re
from functools import reduce
from typing import Optional, Callable, Any, Type, Union

import wx  # type: ignore

from gooey.gui import formatters, events
from gooey.gui.util import wx_util
from gooey.python_bindings.types import FormField
from gooey.util.functional import getin, ifPresent
from gooey.gui.validators import runValidator
from gooey.gui.components.util.wrapped_static_text import AutoWrappedStaticText
from gooey.gui.components.mouse import notifyMouseEvent
from gooey.python_bindings import types as t


class BaseWidget(wx.Panel):
    widget_class: Any

    def arrange(self, label, text):
        raise NotImplementedError

    def getWidget(self, parent: wx.Window, **options):
        return self.widget_class(parent, **options)

    def connectSignal(self):
        raise NotImplementedError

    def getSublayout(self, *args, **kwargs):
        raise NotImplementedError

    def setValue(self, value):
        raise NotImplementedError

    def setPlaceholder(self, value):
        raise NotImplementedError

    def receiveChange(self, *args, **kwargs):
        raise NotImplementedError

    def dispatchChange(self, value, **kwargs):
        raise NotImplementedError

    def formatOutput(self, metatdata, value):
        raise NotImplementedError


class TextContainer(BaseWidget):
    # TODO: fix this busted-ass inheritance hierarchy.
    # Cracking at the seems for more advanced widgets
    # problems:
    #   - all the usual textbook problems of inheritance
    #   - assumes there will only ever be ONE widget created
    #   - assumes those widgets are all created in `getWidget`
    #   - all the above make for extremely awkward lifecycle management
    #      - no clear point at which binding is correct.
    #   - I think the core problem here is that I couple the interface
    #     for shared presentation layout with the specification of
    #     a behavioral interface
    #     - This should be broken apart.
    #     - presentation can be ad-hoc or composed
    #     - behavioral just needs a typeclass of get/set/format for Gooey's purposes
    widget_class = None  # type: ignore

    def __init__(self, parent, widgetInfo, *args, **kwargs):
        super(TextContainer, self).__init__(parent, *args, **kwargs)

        self.info = widgetInfo
        self._id = widgetInfo['id']
        self.widgetInfo = widgetInfo
        self._meta = widgetInfo['data']
        self._options = widgetInfo['options']
        self.label = wx.StaticText(self, label=widgetInfo['data']['display_name'])
        self.help_text = AutoWrappedStaticText(self, label=widgetInfo['data']['help'] or '')
        self.error = AutoWrappedStaticText(self, label='')
        self.error.Hide()
        self.widget = self.getWidget(self)
        self.layout = self.arrange(*args, **kwargs)
        self.setColors()
        self.SetSizer(self.layout)
        self.bindMouseEvents()
        self.Bind(wx.EVT_SIZE, self.onSize)

        # 1.0.7 initial_value should supersede default when both are present
        if self._options.get('initial_value') is not None:
            self.setValue(self._options['initial_value'])
        # Checking for None instead of truthiness means False-evaluaded defaults can be used.
        elif self._meta['default'] is not None:
            self.setValue(self._meta['default'])

        if self._options.get('placeholder'):
            self.setPlaceholder(self._options.get('placeholder'))

        self.onComponentInitialized()

    def onComponentInitialized(self):
        pass

    def bindMouseEvents(self):
        """
        Send any LEFT DOWN mouse events to interested
        listeners via pubsub. see: gooey.gui.mouse for background.
        """
        self.Bind(wx.EVT_LEFT_DOWN, notifyMouseEvent)
        self.label.Bind(wx.EVT_LEFT_DOWN, notifyMouseEvent)
        self.help_text.Bind(wx.EVT_LEFT_DOWN, notifyMouseEvent)
        self.error.Bind(wx.EVT_LEFT_DOWN, notifyMouseEvent)
        self.widget.Bind(wx.EVT_LEFT_DOWN, notifyMouseEvent)

    def arrange(self, *args, **kwargs):
        wx_util.make_bold(self.label)
        wx_util.withColor(self.label, self._options['label_color'])
        wx_util.withColor(self.help_text, self._options['help_color'])
        wx_util.withColor(self.error, self._options['error_color'])

        self.help_text.SetMinSize((0,-1))

        layout = wx.BoxSizer(wx.VERTICAL)

        if self._options.get('show_label', True):
            layout.Add(self.label, 0, wx.EXPAND)
        else:
            self.label.Show(False)
            layout.AddStretchSpacer(1)

        layout.AddSpacer(2)
        if self.help_text and self._options.get('show_help', True):
            layout.Add(self.help_text, 1, wx.EXPAND)
            layout.AddSpacer(2)
        else:
            self.help_text.Show(False)
            layout.AddStretchSpacer(1)
        layout.Add(self.getSublayout(), 0, wx.EXPAND)
        layout.Add(self.error, 1, wx.EXPAND)

        # self.error.SetLabel("HELLOOOOO??")
        # self.error.Show()
        # print(self.error.Shown)
        return layout


    def setColors(self):
        wx_util.make_bold(self.label)
        wx_util.withColor(self.label, self._options['label_color'])
        wx_util.withColor(self.help_text, self._options['help_color'])
        wx_util.withColor(self.error, self._options['error_color'])
        if self._options.get('label_bg_color'):
            self.label.SetBackgroundColour(self._options.get('label_bg_color'))
        if self._options.get('help_bg_color'):
            self.help_text.SetBackgroundColour(self._options.get('help_bg_color'))
        if self._options.get('error_bg_color'):
            self.error.SetBackgroundColour(self._options.get('error_bg_color'))

    def getWidget(self, *args, **options):
        return self.widget_class(*args, **options)

    def getWidgetValue(self):
        raise NotImplementedError

    def getSublayout(self, *args, **kwargs):
        layout = wx.BoxSizer(wx.HORIZONTAL)
        layout.Add(self.widget, 1, wx.EXPAND)
        return layout

    def onSize(self, event):
        # print(self.GetSize())
        # self.error.Wrap(self.GetSize().width)
        # self.help_text.Wrap(500)
        # self.Layout()
        event.Skip()

    def getUiState(self) -> t.FormField:
        return t.TextField(
            id=self._id,
            type=self.widgetInfo['type'],
            value=self.getWidgetValue(),
            placeholder=self.widget.widget.GetHint(),
            error=self.error.GetLabel().replace('\n', ' '),
            enabled=self.IsEnabled(),
            visible=self.IsShown()
        )

    def syncUiState(self, state: FormField):  # type: ignore
        self.widget.setValue(state['value'])  # type: ignore
        self.error.SetLabel(state['error'] or '')
        self.error.Show(state['error'] is not None and state['error'] is not '')


    def getValue(self) -> t.FieldValue:
        regexFunc: Callable[[str], bool] = lambda x: bool(re.match(userValidator, x))

        userValidator = getin(self._options, ['validator', 'test'], 'True')
        message = getin(self._options, ['validator', 'message'], '')
        testFunc = regexFunc \
                   if getin(self._options, ['validator', 'type'], None) == 'RegexValidator'\
                   else eval('lambda user_input: bool(%s)' % userValidator)
        satisfies = testFunc if self._meta['required'] else ifPresent(testFunc)
        value = self.getWidgetValue()
        cmd = self.formatOutput(self._meta, value)
        if 'cli_formatter' in self._options:
            cmd = self._options['cli_formatter'].format(cmd=cmd,
                                                        value=value,
                                                        id=self._id,
                                                        meta=self._meta,
                                                        options=self._options,
                                                        dest=self._meta.get('dest'))

        return t.FieldValue(  # type: ignore
            id=self._id,
            cmd=cmd,
            meta=self._meta,
            rawValue= value,
            # type=self.info['type'],
            enabled=self.IsEnabled(),
            visible=self.IsShown(),
            test= runValidator(satisfies, value),
            error=None if runValidator(satisfies, value) else message,
            clitype=('positional'
                        if self._meta['required'] and not self._meta['commands']
                        else 'optional')
        )

    def setValue(self, value):
        self.widget.SetValue(value)

    def setPlaceholder(self, value):
        if getattr(self.widget, 'SetHint', None):
            self.widget.SetHint(value)

    def setErrorString(self, message):
        self.error.SetLabel(message)
        self.error.Wrap(self.Size.width)
        self.Layout()

    def showErrorString(self, b):
        self.error.Wrap(self.Size.width)
        self.error.Show(b)

    def setOptions(self, values):
        return None

    def receiveChange(self, metatdata, value):
        raise NotImplementedError

    def dispatchChange(self, value, **kwargs):
        raise NotImplementedError

    def formatOutput(self, metadata, value) -> str:
        raise NotImplementedError




class BaseChooser(TextContainer):
    """ Base Class for the Chooser widget types """

    def setValue(self, value):
        self.widget.setValue(value)

    def setPlaceholder(self, value):
        self.widget.SetHint(value)

    def getWidgetValue(self):
        return self.widget.getValue()

    def formatOutput(self, metatdata, value):
        return formatters.general(metatdata, value)

    def getUiState(self) -> t.FormField:
        btn: wx.Button = self.widget.button  # type: ignore
        return t.Chooser(
            id=self._id,
            type=self.widgetInfo['type'],
            value=self.widget.getValue(),
            btn_label=btn.GetLabel(),
            error=self.error.GetLabel() or None,
            enabled=self.IsEnabled(),
            visible=self.IsShown()
        )
