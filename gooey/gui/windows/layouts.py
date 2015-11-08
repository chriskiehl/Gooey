from collections import OrderedDict
import wx
from gooey.gui.pubsub import pub

from gooey.gui import events
from gooey.gui.windows.advanced_config import ConfigPanel
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

    self.main_content = ConfigPanel(self, widgets=self._build_spec['widgets'], opt_cols=self._build_spec['num_optional_cols'])

    sizer = wx.BoxSizer(wx.HORIZONTAL)
    sizer.Add(self.main_content, 3, wx.EXPAND)
    self.SetSizer(sizer)

  def GetOptions(self):
    return self.main_content.GetOptions()

  def GetRequiredArgs(self):
    return self.main_content.GetRequiredArgs()


class ColumnLayout(wx.Panel):
  def __init__(self, *args, **kwargs):
    self._build_spec = kwargs.pop('build_spec')
    super(ColumnLayout, self).__init__(*args, **kwargs)
    self.SetDoubleBuffered(True)

    self.sidebar = Sidebar(self, contents=self._build_spec['widgets'].keys())

    self.config_panels = self.build_panels(self._build_spec)
    self.active_panel = self.config_panels.keys()[0]
    self.config_panels[self.active_panel].Show()

    sizer = wx.BoxSizer(wx.HORIZONTAL)
    sizer.Add(self.sidebar, 1, wx.EXPAND)
    sizer.Add(wx_util.vertical_rule(self), 0, wx.EXPAND)
    for panel in self.config_panels.values():
      sizer.Add(panel, 3, wx.EXPAND)
    self.SetSizer(sizer)

    pub.subscribe(self.load_view,   events.PANEL_CHANGE)

  def load_view(self, view_name):
    self.config_panels[self.active_panel].Hide()
    self.config_panels[view_name].Show()
    self.active_panel = view_name
    self.Layout()

  def build_panels(self, build_spec):
    panels = OrderedDict()
    for panel_name in self._build_spec['widgets'].keys():
      panel = ConfigPanel(self, widgets=self._build_spec['widgets'][panel_name], opt_cols=self._build_spec['num_optional_cols'], title=panel_name.upper())
      panels[panel_name] = panel
      panel.Hide()
    return panels

  def GetOptions(self):
    return '{} {}'.format(self.active_panel, self.config_panels[self.active_panel].GetOptions())

  def GetRequiredArgs(self):
    return self.config_panels[self.active_panel].GetRequiredArgs()



def get_layout_builder(layout_type):
  if layout_type == 'column':
    return

