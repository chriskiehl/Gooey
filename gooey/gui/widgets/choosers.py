from gooey.gui.lang import i18n

__author__ = 'Chris'

import wx

from gooey.gui.util import wx_util
from gooey.gui.widgets.calender_dialog import CalendarDlg


class AbstractChooser(object):
  def __init__(self, data):
    self.data = data

    # parent
    self.panel = None

    self.button_text = i18n._('browse')

    # Widgets
    self.title = None
    self.help_msg = None
    self.text_box = None
    self.button = None
    self.panel = None

  def build(self, parent):
    return self.do_layout(parent)

  def do_layout(self, parent):
    self.panel = wx.Panel(parent)
    self.panel.SetDoubleBuffered(True)
    self.title = self.CreateNameLabelWidget(self.panel)
    self.help_msg = self.CreateHelpMsgWidget(self.panel)
    self.text_box = wx.TextCtrl(self.panel)
    self.button = wx.Button(self.panel, label=self.button_text, size=(73, 23))

    vertical_container = wx.BoxSizer(wx.VERTICAL)
    widget_sizer = wx.BoxSizer(wx.HORIZONTAL)

    vertical_container.Add(self.title)
    vertical_container.AddSpacer(2)

    if self.help_msg.GetLabelText():
      vertical_container.Add(self.help_msg, 1, wx.EXPAND)
      vertical_container.AddSpacer(2)
    else:
      vertical_container.AddStretchSpacer(1)

    widget_sizer.Add(self.text_box, 1, wx.EXPAND)
    widget_sizer.AddSpacer(10)
    widget_sizer.Add(self.button, 0)

    vertical_container.Add(widget_sizer, 0, wx.EXPAND)
    self.panel.SetSizer(vertical_container)

    self.panel.Bind(wx.EVT_SIZE, self.OnResize)
    self.panel.Bind(wx.EVT_BUTTON, self.on_button, self.button)
    return self.panel

  def CreateHelpMsgWidget(self, parent):
    base_text = wx.StaticText(parent, label=self.data['help_msg'])
    # if self.data['nargs']:
    #   base_text.SetLabelText(base_text.GetLabelText() + self.CreateNargsMsg(action))
    wx_util.dark_grey(base_text)
    return base_text

  def CreateNameLabelWidget(self, parent):
    label = self.data['title'].title()
    text = wx.StaticText(parent, label=label)
    wx_util.make_bold(text)
    return text

  def OnResize(self, evt):
    if self.help_msg is None:
      return

    container_width, _ = self.panel.Size
    text_width, _ = self.help_msg.Size

    if text_width != container_width:
      self.help_msg.SetLabel(self.help_msg.GetLabelText().replace('\n', ' '))
      self.help_msg.Wrap(container_width)
    evt.Skip()

  def on_button(self, evt):
    raise NotImplementedError



class FileChooser(AbstractChooser):
  def __init__(self, data):
    AbstractChooser.__init__(self, data)

  def on_button(self, evt):
    dlg = wx.FileDialog(self.panel, style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
    result = (dlg.GetPath()
              if dlg.ShowModal() == wx.ID_OK
              else None)
    if result:
      self.text_box.SetLabelText(result)


class DirectoryChooser(AbstractChooser):
  def __init__(self, data):
    AbstractChooser.__init__(self, data)

  def on_button(self, evt):
    dlg = wx.DirDialog(self.panel, 'Select directory', style=wx.DD_DEFAULT_STYLE)
    result = (dlg.GetPath()
              if dlg.ShowModal() == wx.ID_OK
              else None)
    if result:
      self.text_box.SetLabelText(result)


class CalendarChooser(AbstractChooser):
  def __init__(self, data):
    AbstractChooser.__init__(self, data)
    self.button_text = 'Choose Date'

  def on_button(self, evt):
    dlg = CalendarDlg(self.panel)
    dlg.ShowModal()
    if dlg.GetPath():
      self.text_box.SetLabelText(dlg.GetPath())

















