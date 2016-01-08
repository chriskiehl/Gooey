from functools import partial

import wx

from gooey.gui.util import wx_util
from gooey.gui.widgets import widget_pack


class BaseGuiComponent(object):

  widget_class = None

  def __init__(self, parent, title, msg):
    '''
    :param data: field info (title, help, etc..)
    :param widget_pack: internal wxWidgets to render
    '''
    # parent
    self.parent = parent

    # Widgets
    self.title = None
    self.help_msg = None

    # Internal WidgetPack set in subclasses

    self.do_layout(parent, title, msg)

  def do_layout(self, parent, title, msg):
    self.panel = wx.Panel(parent)

    self.widget_pack = self.widget_class()

    self.title = self.format_title(self.panel, title)
    self.help_msg = self.format_help_msg(self.panel, msg)
    self.help_msg.SetMinSize((0, -1))
    core_widget_set = self.widget_pack.build(self.panel, {})

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
    print self.widget_pack.widget.Bind(*args, **kwargs)

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

  # def HasOptionString(self):
  #   return bool(self.widget_pack.option_string)
  #
  # def _GetWidget(self):
  #   # used only for unittesting
  #   return self.widget_pack.widget

  def __repr__(self):
    return self.__class__.__name__


class CheckBox(BaseGuiComponent):

  def __init__(self, parent, title, msg):
    BaseGuiComponent.__init__(self, parent, title, msg)

  def do_layout(self, parent, title, msg):
    self.panel = wx.Panel(parent)

    self.widget = wx.CheckBox(self.panel)
    # self.widget.SetValue(self.default_value)
    self.title = self.format_title(self.panel, title)
    self.help_msg = self.format_help_msg(self.panel, msg)
    self.help_msg.SetMinSize((0, -1))

    # self.help_msg.Bind(wx.EVT_LEFT_UP, lambda event: self.widget.SetValue(not self.widget.GetValue()))

    vertical_container = wx.BoxSizer(wx.VERTICAL)
    vertical_container.Add(self.title)

    horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)
    horizontal_sizer.Add(self.widget, 0, wx.EXPAND | wx.RIGHT, 10)
    horizontal_sizer.Add(self.help_msg, 1, wx.EXPAND)

    vertical_container.Add(horizontal_sizer, 0, wx.EXPAND)

    self.panel.SetSizer(vertical_container)
    self.panel.Bind(wx.EVT_SIZE, self.onResize)
    return self.panel

  def onResize(self, evt):
    msg = self.help_msg
    container_width, _ = self.panel.Size
    text_width, _ = msg.Size

    if text_width != container_width:
      msg.SetLabel(msg.GetLabelText().replace('\n', ' '))
      msg.Wrap(container_width)
    evt.Skip()

  def get_value(self):
    return self.widget.GetValue()

  def set_value(self, val):
    self.widget.SetValue(val)


  # def GetValue(self):
  #   return self.option_strings if self.widget.GetValue() else ''
  #
  # def HasOptionString(self):
  #   return bool(self.option_strings)
  #
  # def _GetWidget(self):
  #   return self.widget


class RadioGroup(object):
  def __init__(self, parent, title, msg):
    self.panel = None

    # self.data = data

    self.radio_buttons = []
    self.option_strings = []
    self.help_msgs = []
    self.btn_names = []

    self.do_layout(parent, title, msg)

  def do_layout(self, parent, titles, msgs):
    self.panel = wx.Panel(parent)

    self.radio_buttons = [wx.RadioButton(self.panel, -1) for _ in titles]
    self.btn_names = [wx.StaticText(self.panel, label=title.title()) for title in titles]
    self.help_msgs = [wx.StaticText(self.panel, label=msg.title()) for msg in msgs]

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
    self.panel.Bind(wx.EVT_RADIOBUTTON, self.showz)
    return self.panel

  def showz(self, evt):
    print evt
    for i in self.radio_buttons:
      print i.GetValue()

  def onResize(self, evt):
    msg = self.help_msgs[0]
    container_width, _ = self.panel.Size
    text_width, _ = msg.Size

    if text_width != container_width:
      msg.SetLabel(msg.GetLabelText().replace('\n', ' '))
      msg.Wrap(container_width)
    evt.Skip()

  def get_value(self):
    return [button.GetValue() for button in self.radio_buttons]

  def set_value(self, val):
    pass

  # def GetValue(self):
  #   vals = [button.GetValue() for button in self.radio_buttons]
  #   try:
  #     return self.option_strings[vals.index(True)][0]
  #   except:
  #     return ''

  def HasOptionString(self):
    return bool(self.option_strings)

  def _GetWidget(self):
    return self.radio_buttons


def build_subclass(name, widget_class):
  # this seemed faster than typing class X a bunch
  return type(name, (BaseGuiComponent,), {'widget_class': widget_class})


FileChooser       = build_subclass('FileChooser', widget_pack.FileChooserPayload)
MultiFileChooser  = build_subclass('MultiFileChooser', widget_pack.MultiFileSaverPayload)
DirChooser        = build_subclass('DirChooser', widget_pack.DirChooserPayload)
FileSaver         = build_subclass('FileSaver', widget_pack.FileSaverPayload)
DateChooser       = build_subclass('DateChooser', widget_pack.DateChooserPayload)
TextField         = build_subclass('TextField', widget_pack.TextInputPayload)
CommandField      = build_subclass('CommandField', widget_pack.TextInputPayload(no_quoting=True))
Dropdown          = build_subclass('Dropdown', widget_pack.DropdownPayload)
Counter           = build_subclass('Counter', widget_pack.CounterPayload)
MultiDirChooser   = build_subclass('MultiDirChooser', widget_pack.MultiDirChooserPayload)

if __name__ == '__main__':

  DirChooser = type('DirChooser', (BaseGuiComponent,), {'widget_pack': widget_pack.DirChooserPayload })
  d = DirChooser()
