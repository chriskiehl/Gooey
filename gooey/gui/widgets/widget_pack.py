from functools import partial
from gooey.gui.lang import i18n
from gooey.gui.util.filedrop import FileDrop

__author__ = 'Chris'

from abc import ABCMeta, abstractmethod

import wx

from gooey.gui.widgets.calender_dialog import CalendarDlg


class WidgetPack(object):
  """
  Interface specifying the contract to which
  all `WidgetPack`s will adhere
  """
  __metaclass__ = ABCMeta

  @abstractmethod
  def build(self, parent, data):
    pass

  @abstractmethod
  def getValue(self):
    pass

  def onResize(self, evt):
    pass

  @staticmethod
  def get_command(data):
    return data['commands'][0] if data['commands'] else ''




class BaseChooser(WidgetPack):
  def __init__(self, button_text=''):
    self.button_text = i18n._('browse')
    self.option_string = None
    self.parent = None
    self.text_box = None
    self.button = None

  def build(self, parent, data=None):
    self.parent = parent
    self.option_string = data['commands'][0] if data['commands'] else ''
    self.text_box = wx.TextCtrl(self.parent)
    self.text_box.SetMinSize((0, -1))
    dt = FileDrop(self.text_box)
    self.text_box.SetDropTarget(dt)
    self.button = wx.Button(self.parent, label=self.button_text, size=(73, 23))

    widget_sizer = wx.BoxSizer(wx.HORIZONTAL)
    widget_sizer.Add(self.text_box, 1, wx.EXPAND)
    widget_sizer.AddSpacer(10)
    widget_sizer.Add(self.button, 0)

    parent.Bind(wx.EVT_BUTTON, self.onButton, self.button)
    return widget_sizer

  def getValue(self):
    value = self.text_box.GetValue()
    if self.option_string and value:
      return '{0} "{1}"'.format(self.option_string, value)
    else:
      return '"{}"'.format(value) if value else ''

  def onButton(self, evt):
    raise NotImplementedError


  def __repr__(self):
    return self.__class__.__name__


class BaseFileChooser(BaseChooser):
  def __init__(self, dialog):
    BaseChooser.__init__(self)
    self.dialog = dialog

  def onButton(self, evt):
    dlg = self.dialog(self.parent)
    result = (self.get_path(dlg)
              if dlg.ShowModal() == wx.ID_OK
              else None)
    if result:
      self.text_box.SetValue(result)

  def get_path(self, dlg):
    if isinstance(dlg, wx.DirDialog):
      return dlg.GetPath()
    else:
      paths = dlg.GetPaths()
      return paths[0] if len(paths) < 2 else ' '.join(paths)

def build_dialog(style, exist_constraint=True, **kwargs):
  if exist_constraint:
    return lambda panel: wx.FileDialog(panel, style=style | wx.FD_FILE_MUST_EXIST, **kwargs)
  else:
    return lambda panel: wx.FileDialog(panel, style=style, **kwargs)


FileChooserPayload    = partial(BaseFileChooser, dialog=build_dialog(wx.FD_OPEN))
FileSaverPayload      = partial(BaseFileChooser, dialog=build_dialog(wx.FD_SAVE, False, defaultFile="Enter Filename"))
MultiFileSaverPayload = partial(BaseFileChooser, dialog=build_dialog(wx.FD_MULTIPLE, False))
DirChooserPayload     = partial(BaseFileChooser, dialog=lambda parent: wx.DirDialog(parent, 'Select Directory', style=wx.DD_DEFAULT_STYLE))
DateChooserPayload    = partial(BaseFileChooser, dialog=CalendarDlg)
MultiDirChooserPayload = partial(BaseFileChooser, dialog=lambda parent: wx.DirDialog(parent, 'Select Directory', style=wx.DD_DEFAULT_STYLE | wx.DIRCTRL_MULTIPLE))

class TextInputPayload(WidgetPack):
  def __init__(self):
    self.widget = None
    self.option_string = None

  def build(self, parent, data):
    self.option_string = self.get_command(data)
    self.widget = wx.TextCtrl(parent)
    dt = FileDrop(self.widget)
    self.widget.SetDropTarget(dt)
    self.widget.SetMinSize((0, -1))
    self.widget.SetDoubleBuffered(True)
    return self.widget

  def getValue(self):
    value = self.widget.GetValue()
    if value and self.option_string:
      return '{} {}'.format(self.option_string, value)
    else:
      return '"{}"'.format(value) if value else ''

  def _SetValue(self, text):
    # used for testing
    self.widget.SetLabelText(text)


class DropdownPayload(WidgetPack):
  default_value = 'Select Option'

  def __init__(self):
    self.option_string = None
    self.widget = None

  def build(self, parent, data):
    self.option_string = self.get_command(data)
    self.widget = wx.ComboBox(
      parent=parent,
      id=-1,
      value=self.default_value,
      choices=data['choices'],
      style=wx.CB_DROPDOWN
    )
    return self.widget

  def getValue(self):
    if self.widget.GetValue() == self.default_value:
      return ''
    elif self.widget.GetValue() and self.option_string:
      return '{} {}'.format(self.option_string, self.widget.GetValue())
    else:
      self.widget.GetValue()

  def _SetValue(self, text):
    # used for testing
    self.widget.SetLabelText(text)


class CounterPayload(WidgetPack):
  def __init__(self):
    self.option_string = None
    self.widget = None

  def build(self, parent, data):
    self.option_string = self.get_command(data)
    self.widget = wx.ComboBox(
      parent=parent,
      id=-1,
      value='',
      choices=[str(x) for x in range(1, 7)],
      style=wx.CB_DROPDOWN
    )
    return self.widget

  def getValue(self):
    '''
    Returns
      str(option_string * DropDown Value)
      e.g.
      -vvvvv
    '''
    dropdown_value = self.widget.GetValue()
    if not str(dropdown_value).isdigit():
      return ''
    arg = str(self.option_string).replace('-', '')
    repeated_args = arg * int(dropdown_value)
    return '-' + repeated_args


