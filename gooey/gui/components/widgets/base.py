import wx

from gooey.gui.util import wx_util




class BaseWidget(wx.Panel):

    def __init__(self, parent, *args, **kwargs ):
        super(BaseWidget, self).__init__(*args, **kwargs)


    def arrange(self, label, text):
        raise NotImplementedError

    def getWidget(self, ):
        return self.widget_class(self)

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
    '''

    type: "N"
    validator: "x > 10 and x < 11"

    '''
    widget_class = None

    def __init__(self, parent, widgetInfo, *args, **kwargs):
        super(TextContainer, self).__init__(parent, *args, **kwargs)

        self._id = widgetInfo['id']
        self._meta = widgetInfo['data']
        self.label = wx.StaticText('<b>{}</b>'.format(widgetInfo['data']['display_name']))
        self.help_text = wx.StaticText(widgetInfo['data']['help'])
        self.error_text = wx.StaticText(widgetInfo['data']['help'])
        self.widget = self.getWidget()
        self.layout = self.arrange(self.label, self.help_text)
        self.value = Subject()
        self.connectSignal()

    def arrange(self, label, text):
        layout = QVBoxLayout()
        layout.addWidget(label, alignment=Qt.AlignTop)
        if text:
            layout.addWidget(text)
        else:
            layout.addStretch(1)
        layout.addLayout(self.getSublayout())
        return layout

    def getWidget(self,):
        return self.widget_class(self)

    def connectSignal(self):
        self.widget.textChanged.connect(self.dispatchChange)

    def getSublayout(self, *args, **kwargs):
        raise NotImplementedError

    def setValue(self, value):
        raise NotImplementedError

    def receiveChange(self, metatdata, value):
        raise NotImplementedError

    def dispatchChange(self, value, **kwargs):
        raise NotImplementedError

    def formatOutput(self, metadata, value):
        raise NotImplementedError




class BaseGuiComponent(object):
    widget_class = None

    def __init__(self, parent, title, msg, choices=None):
        '''
        :param data: field info (title, help, etc..)
        :param widget_pack: internal wxWidgets to render
        '''
        # parent
        self.parent = parent

        # Widgets
        self.title = None
        self.help_msg = None
        self.choices = choices

        # Internal WidgetPack set in subclasses

        self.do_layout(parent, title, msg)

    def do_layout(self, parent, title, msg):
        self.panel = wx.Panel(parent)

        self.widget_pack = self.widget_class()

        self.title = self.format_title(self.panel, title)
        self.help_msg = self.format_help_msg(self.panel, msg)
        self.help_msg.SetMinSize((0, -1))
        core_widget_set = self.widget_pack.build(self.panel, {}, self.choices)

        vertical_container = wx.BoxSizer(wx.VERTICAL)

        vertical_container.Add(self.title)
        vertical_container.AddSpacer(2)

        if self.help_msg.GetLabelText():
            vertical_container.Add(self.help_msg, 1, wx.EXPAND)
            vertical_container.AddSpacer(2)
        else:
            vertical_container.AddStretchSpacer(1)

        vertical_container.Add(core_widget_set, 0, wx.EXPAND)
        self.panel.SetSizer(vertical_container)

        return self.panel

    def bind(self, *args, **kwargs):
        print(self.widget_pack.widget.Bind(*args, **kwargs))

    def get_title(self):
        return self.title.GetLabel()

    def set_title(self, text):
        self.title.SetLabel(text)

    def get_help_msg(self):
        return self.help_msg.GetLabelText()

    def set_label_text(self, text):
        self.help_msg.SetLabel(text)

    def format_help_msg(self, parent, msg):
        base_text = wx.StaticText(parent, label=msg or '')
        wx_util.dark_grey(base_text)
        return base_text

    def format_title(self, parent, title):
        text = wx.StaticText(parent, label=title)
        wx_util.make_bold(text)
        return text

    def onResize(self, evt):
        # handle internal widgets
        # self.panel.Freeze()
        self._onResize(evt)
        # propagate event to child widgets
        self.widget_pack.onResize(evt)
        evt.Skip()
        # self.panel.Thaw()

    def _onResize(self, evt):
        if not self.help_msg:
            return
        self.panel.Size = evt.GetSize()
        container_width, _ = self.panel.Size
        text_width, _ = self.help_msg.Size

        if text_width != container_width:
            self.help_msg.SetLabel(self.help_msg.GetLabelText().replace('\n', ' '))
            self.help_msg.Wrap(container_width)
        evt.Skip()

    def get_value(self):
        return self.widget_pack.get_value()

    def set_value(self, val):
        if val:
            self.widget_pack.widget.SetValue(str(val))

    def __repr__(self):
        return self.__class__.__name__
