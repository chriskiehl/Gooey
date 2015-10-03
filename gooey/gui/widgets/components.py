import wx

from gooey.gui.util import wx_util
from gooey.gui.widgets import widget_pack


class BaseGuiComponent(object):
  def __init__(self, data, widget_pack):
    '''
    :param data: field info (title, help, etc..)
    :param widget_pack: internal wxWidgets to render
    '''
    self.data = data

    # parent
    self.panel = None

    # Widgets
    self.title = None
    self.help_msg = None

    # Internal WidgetPack
    self.widget_pack = widget_pack

  def build(self, parent):
    return self.do_layout(parent)

  def do_layout(self, parent):
    self.panel = wx.Panel(parent)


    self.title = self.createTitle(self.panel)
    self.help_msg = self.createHelpMsgWidget(self.panel)
    self.help_msg.SetMinSize((0, -1))
    core_widget_set = self.widget_pack.build(self.panel, self.data)

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

    # self.panel.Bind(wx.EVT_SIZE, self.onResize)
    return self.panel

  def createHelpMsgWidget(self, parent):
    label_text = (self.formatExtendedHelpMsg(self.data)
                  if self.data['nargs']
                  else self.data['help'])
    base_text = wx.StaticText(parent, label=label_text or '')
    wx_util.dark_grey(base_text)
    return base_text

  def createTitle(self, parent):
    text = wx.StaticText(parent, label=self.data['display_name'].title())
    wx_util.make_bold(text)
    return text

  def formatExtendedHelpMsg(self, data):
    base_text = data.get('help', '')
    nargs = data['nargs']
    if isinstance(nargs, int):
      return '{base}\n(Note: exactly {nargs} arguments are required)'.format(base=base_text, nargs=nargs)
    elif nargs == '+':
      return '{base}\n(Note: at least 1 or more arguments are required)'.format(base=base_text)
    return base_text

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

  def GetValue(self):
    return self.widget_pack.getValue()

  def _GetWidget(self):
    # used only for unittesting
    return self.widget_pack.widget

  def __repr__(self):
    return self.__class__.__name__


class CheckBox(BaseGuiComponent):
  def __init__(self, data, widget_pack=None):
    BaseGuiComponent.__init__(self, data, widget_pack)

    self.widget = None
    #  data
    self.option_strings = data['commands'][0]

  def build(self, parent):
    return self.do_layout(parent)

  def do_layout(self, parent):
    self.panel = wx.Panel(parent)

    self.widget = wx.CheckBox(self.panel)
    self.title = self.createTitle(self.panel)
    self.help_msg = self.createHelpMsgWidget(self.panel)
    self.help_msg.SetMinSize((0, -1))

    self.help_msg.Bind(wx.EVT_LEFT_UP, lambda event: self.widget.SetValue(not self.widget.GetValue()))

    vertical_container = wx.BoxSizer(wx.VERTICAL)
    vertical_container.Add(self.title)

    horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)
    horizontal_sizer.Add(self.widget, 0, wx.EXPAND | wx.RIGHT, 10)
    horizontal_sizer.Add(self.help_msg, 1, wx.EXPAND)

    vertical_container.Add(horizontal_sizer, 0, wx.EXPAND)

    self.panel.SetSizer(vertical_container)
    self.panel.Bind(wx.EVT_SIZE, self.onResize)
    return self.panel

  def onSetter(self, evt):
    self.getValue()

  def onResize(self, evt):
    msg = self.help_msg
    container_width, _ = self.panel.Size
    text_width, _ = msg.Size

    if text_width != container_width:
      msg.SetLabel(msg.GetLabelText().replace('\n', ' '))
      msg.Wrap(container_width)
    evt.Skip()

  def GetValue(self):
    return self.option_strings if self.widget.GetValue() else ''

  def _GetWidget(self):
    return self.widget


class RadioGroup(object):
  def __init__(self, data):
    self.panel = None

    self.data = data

    self.radio_buttons = []
    self.option_stings = []
    self.help_msgs = []
    self.btn_names = []

  def build(self, parent):
    return self.do_layout(parent)

  def do_layout(self, parent):
    self.panel = wx.Panel(parent)

    self.radio_buttons = [wx.RadioButton(self.panel, -1) for _ in self.data]
    self.btn_names = [wx.StaticText(self.panel, label=btn_data['display_name'].title()) for btn_data in self.data]
    self.help_msgs = [wx.StaticText(self.panel, label=btn_data['help'].title()) for btn_data in self.data]
    self.option_stings = [btn_data['commands'] for btn_data in self.data]

    # box = wx.StaticBox(self.panel, -1, label=self.data['group_name'])
    box = wx.StaticBox(self.panel, -1, label='')
    vertical_container = wx.StaticBoxSizer(box, wx.VERTICAL)

    for button, name, help in zip(self.radio_buttons, self.btn_names, self.help_msgs):

      hbox = wx.BoxSizer(wx.HORIZONTAL)

      hbox.Add(button, 0, wx.ALIGN_TOP | wx.ALIGN_LEFT)
      hbox.Add(name, 0, wx.LEFT, 10)

      vertical_container.Add(hbox, 0, wx.EXPAND)

      vertical_container.Add(help, 1, wx.EXPAND | wx.LEFT, 25)
      vertical_container.AddSpacer(5)
      # self.panel.Bind(wx.EVT_RADIOBUTTON, self.onSetter, button)

    self.panel.SetSizer(vertical_container)
    self.panel.Bind(wx.EVT_SIZE, self.onResize)
    return self.panel

  def onSetter(self, evt):
    self.getValue()

  def onResize(self, evt):
    msg = self.help_msgs[0]
    container_width, _ = self.panel.Size
    text_width, _ = msg.Size

    if text_width != container_width:
      msg.SetLabel(msg.GetLabelText().replace('\n', ' '))
      msg.Wrap(container_width)
    evt.Skip()

  def GetValue(self):
    vals = [button.GetValue() for button in self.radio_buttons]
    try:
      return self.option_stings[vals.index(True)][0]
    except:
      return ''

  def _GetWidget(self):
    return self.radio_buttons


FileChooser       = lambda data: BaseGuiComponent(data=data, widget_pack=widget_pack.FileChooserPayload())
MultiFileChooser  = lambda data: BaseGuiComponent(data=data, widget_pack=widget_pack.MultiFileSaverPayload())
DirChooser        = lambda data: BaseGuiComponent(data=data, widget_pack=widget_pack.DirChooserPayload())
FileSaver         = lambda data: BaseGuiComponent(data=data, widget_pack=widget_pack.FileSaverPayload())
DateChooser       = lambda data: BaseGuiComponent(data=data, widget_pack=widget_pack.DateChooserPayload())
TextField         = lambda data: BaseGuiComponent(data=data, widget_pack=widget_pack.TextInputPayload())
Dropdown          = lambda data: BaseGuiComponent(data=data, widget_pack=widget_pack.DropdownPayload())
Counter           = lambda data: BaseGuiComponent(data=data, widget_pack=widget_pack.CounterPayload())
MultiDirChooser   = lambda data: BaseGuiComponent(data=data, widget_pack=widget_pack.MultiDirChooserPayload())

