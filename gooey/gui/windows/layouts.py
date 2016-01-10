import wx

from gooey.gui.util import wx_util
from gooey.gui.windows.advanced_config import ConfigPanel
from gooey.gui.windows.sidebar import Sidebar

basic_config = {
    'widgets': [{
      'type': 'CommandField',
      'required': True,
      'data': {
        'display_name': 'Enter Commands',
        'help': 'Enter command line arguments',
        'nargs': '',
        'commands': '',
        'choices': [],
        'default': None,
      }
    }],
}


FLAT = 'standard'
COLUMN = 'column'


class FlatLayout(wx.Panel):
  def __init__(self, *args, **kwargs):
    super(FlatLayout, self).__init__(*args, **kwargs)
    self.SetDoubleBuffered(True)

    self.main_content = ConfigPanel(self, opt_cols=3)

    sizer = wx.BoxSizer(wx.HORIZONTAL)
    sizer.Add(self.main_content, 3, wx.EXPAND)
    self.SetSizer(sizer)


class ColumnLayout(wx.Panel):
  def __init__(self, *args, **kwargs):
    super(ColumnLayout, self).__init__(*args, **kwargs)
    self.SetDoubleBuffered(True)

    self.sidebar = Sidebar(self)
    self.main_content = ConfigPanel(self, opt_cols=2)

    sizer = wx.BoxSizer(wx.HORIZONTAL)
    sizer.Add(self.sidebar, 1, wx.EXPAND)
    sizer.Add(wx_util.vertical_rule(self), 0, wx.EXPAND)
    sizer.Add(self.main_content, 3, wx.EXPAND)
    self.SetSizer(sizer)


