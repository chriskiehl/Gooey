import wx
# from rx.subjects import Subject

from gooey.gui import formatters, events
from gooey.gui.pubsub import pub
from gooey.gui.util import wx_util
from gooey.util.functional import getin, ifPresent
from gooey.gui.validators import runValidator


class BaseWidget(wx.Panel):
    widget_class = None

    def arrange(self, label, text):
        raise NotImplementedError

    def getWidget(self, parent, **options):
        return self.widget_class(parent, **options)

    def connectSignal(self):
        raise NotImplementedError

    def getSublayout(self, *args, **kwargs):
        raise NotImplementedError

    def setValue(self, value):
        raise NotImplementedError

    def receiveChange(self, *args, **kwargs):
        raise NotImplementedError

    def dispatchChange(self, value, **kwargs):
        raise NotImplementedError

    def formatOutput(self, metatdata, value):
        raise NotImplementedError


class TextContainer(BaseWidget):
    widget_class = None

    def __init__(self, parent, widgetInfo, *args, **kwargs):
        super(TextContainer, self).__init__(parent, *args, **kwargs)

        self.info = widgetInfo
        self._id = widgetInfo['id']
        self._meta = widgetInfo['data']
        self._options = widgetInfo['options']
        self.label = wx.StaticText(self, label=widgetInfo['data']['display_name'])
        self.help_text = wx.StaticText(self, label=widgetInfo['data']['help'] or '')
        self.error = wx.StaticText(self, label='')
        self.error.Hide()
        self.widget = self.getWidget(self)
        self.layout = self.arrange(*args, **kwargs)
        self.SetSizer(self.layout)
        self.Bind(wx.EVT_SIZE, self.onSize)
        if self._meta['default']:
            self.setValue(self._meta['default'])


    def arrange(self, *args, **kwargs):
        wx_util.make_bold(self.label)
        wx_util.dark_grey(self.help_text)
        wx_util.withColor(self.error, self._options['error_color'])

        self.help_text.SetMinSize((0,-1))

        layout = wx.BoxSizer(wx.VERTICAL)
        layout.Add(self.label)
        layout.AddSpacer(2)
        if self.help_text:
            layout.Add(self.help_text, 1, wx.EXPAND)
            layout.AddSpacer(2)
        else:
            layout.AddStretchSpacer(1)
        layout.Add(self.getSublayout(), 0, wx.EXPAND)
        layout.Add(self.error)
        self.error.Hide()
        return layout

    def getWidget(self, *args, **options):
        return self.widget_class(*args, **options)

    def getWidgetValue(self):
        raise NotImplementedError

    def getSublayout(self, *args, **kwargs):
        layout = wx.BoxSizer(wx.HORIZONTAL)
        layout.Add(self.widget, 1, wx.EXPAND)
        return layout

    def onSize(self, event):
        self.error.Wrap(self.GetSize().width)
        event.Skip()

    def getValue(self):
        userValidator = getin(self._options, ['validator', 'test'], 'True')
        message = getin(self._options, ['validator', 'message'], '')
        testFunc = eval('lambda user_input: bool(%s)' % userValidator)
        satisfies = testFunc if self._meta['required'] else ifPresent(testFunc)
        value = self.getWidgetValue()

        return {
            'id': self._id,
            'cmd': self.formatOutput(self._meta, value),
            'rawValue': value,
            'test': runValidator(satisfies, value),
            'error': None if runValidator(satisfies, value) else message,
            'clitype': 'positional'
                        if self._meta['required'] and not self._meta['commands']
                        else 'optional'
        }

    def setValue(self, value):
        self.widget.SetValue(value)

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

    def formatOutput(self, metadata, value):
        raise NotImplementedError




class BaseChooser(TextContainer):
    """ Base Class for the Chooser widget types """

    def setValue(self, value):
        self.widget.setValue(value)

    def getWidgetValue(self):
        return self.widget.getValue()

    def formatOutput(self, metatdata, value):
        return formatters.general(metatdata, value)
