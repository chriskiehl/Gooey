__author__ = 'Chris'

import wx
import styling

import widget_pack

class BaseGuiComponent(object):
  def __init__(self, data, widget_pack):
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

    self.panel.Bind(wx.EVT_SIZE, self.onResize)
    return self.panel

  def createHelpMsgWidget(self, parent):
    label_text = (self.formatExtendedHelpMsg(self.data)
                  if self.data['nargs']
                  else self.data['help_msg'])
    base_text = wx.StaticText(parent, label=label_text)
    styling.MakeDarkGrey(base_text)
    return base_text

  def createTitle(self, parent):
    text = wx.StaticText(parent, label=self.data['title'].title())
    styling.MakeBold(text)
    return text

  def formatExtendedHelpMsg(self, data):
    base_text = data['help_msg']
    nargs = data['nargs']
    if isinstance(nargs, int):
      return '{base}\n(Note: exactly {nargs} arguments are required)'.format(base=base_text, nargs=nargs)
    elif nargs == '+':
      return '{base}\n(Note: at least 1 or more arguments are required)'.format(base=base_text)
    return base_text

  def onResize(self, evt):
    # handle internal widgets
    self._onResize(evt)
    # propagate event to child widgets
    self.widget_pack.onResize(evt)
    evt.Skip()

  def _onResize(self, evt):
    if self.help_msg is None:
      return
    container_width, _ = self.panel.Size
    text_width, _ = self.help_msg.Size

    if text_width != container_width:
      self.help_msg.SetLabel(self.help_msg.GetLabelText().replace('\n', ' '))
      self.help_msg.Wrap(container_width)

  def getValue(self):
    return self.widget_pack.getValue()


FileChooser = lambda data: BaseGuiComponent(data=data, widget_pack=widget_pack.FileChooserPayload())
DirChooser  = lambda data: BaseGuiComponent(data=data, widget_pack=widget_pack.DirChooserPayload())
DateChooser = lambda data: BaseGuiComponent(data=data, widget_pack=widget_pack.DateChooserPayload())
TextField   = lambda data: BaseGuiComponent(data=data, widget_pack=widget_pack.TextInputPayload())
Dropdown    = lambda data: BaseGuiComponent(data=data, widget_pack=widget_pack.DropdownPayload())
Counter     = lambda data: BaseGuiComponent(data=data, widget_pack=widget_pack.CounterPayload())




