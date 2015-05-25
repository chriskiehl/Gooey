import wx

from gooey.gui.windows.advanced_config import AdvancedConfigPanel
from gooey.gui.windows.sidebar import Sidebar
from gooey.gui.util import wx_util

basic_config = {
    'required': [{
      'type': 'TextField',
      'data': {
        'display_name': 'Enter Commands',
        'help': 'Enter command line arguments',
        'nargs': '',
        'commands': '',
        'choices': [],
      }
    }],
    'optional': []
}


class FlatLayout(wx.Panel):
  def __init__(self, *args, **kwargs):
    self._build_spec = kwargs.pop('build_spec')
    super(FlatLayout, self).__init__(*args, **kwargs)
    self.SetDoubleBuffered(True)

    self.main_content = AdvancedConfigPanel(self, build_spec=self._build_spec)

    sizer = wx.BoxSizer(wx.HORIZONTAL)
    sizer.Add(self.main_content, 3, wx.EXPAND)
    self.SetSizer(sizer)

  def GetOptions(self):
    return self.main_content.GetOptions()

  def GetRequiredArgs(self):
    return self.main_content.GetRequiredArgs()


class ColumnLayout(wx.Panel):
  def __init__(self, *args, **kwargs):
    super(ColumnLayout, self).__init__(*args, **kwargs)
    self.SetDoubleBuffered(True)

    self.sidebar = Sidebar(self, contents=['one', 'two', 'three', 'four', 'five'])
    self.main_content = AdvancedConfigPanel(self)

    sizer = wx.BoxSizer(wx.HORIZONTAL)

    sizer.Add(self.sidebar, 1, wx.EXPAND)
    sizer.Add(wx_util.vertical_rule(self), 0, wx.EXPAND)
    sizer.Add(self.main_content, 3, wx.EXPAND)
    self.SetSizer(sizer)


def get_layout_builder(layout_type):
  if layout_type == 'column':
    return

