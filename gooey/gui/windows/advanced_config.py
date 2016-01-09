"""
Managed the internal layout for configuration options

@author: Chris
"""


import wx
from wx.lib.scrolledpanel import ScrolledPanel
from itertools import chain, izip_longest

from gooey.gui.util import wx_util
from gooey.gui.lang import i18n
from gooey.gui.widgets import components

PADDING = 10


class WidgetContainer(wx.Panel):
  '''
  Collection of widgets
  '''
  def __init__(self, parent, section_name, *args, **kwargs):
    wx.Panel.__init__(self, parent, *args, **kwargs)
    self.section_name = section_name
    self.title = None
    self.widgets = []

    self.container = wx.BoxSizer(wx.VERTICAL)
    self.SetSizer(self.container)

  def populate(self, widgets):
    for index, widget in enumerate(widgets):
      widget_class = getattr(components, widget.type)
      widget_instance = widget_class(self, widget.title, widget.help)
      self.widgets.append(widget_instance)
    self.layout()

  def get_values(self):
    return [x.get_value() for x in self.widgets]

  def layout(self):
    STD_LAYOUT = (0, wx.LEFT | wx.RIGHT | wx.EXPAND, PADDING)

    if self.title:
      self.container.Add(wx_util.h0(self, self.title), 0, wx.LEFT | wx.RIGHT, PADDING)
      self.container.AddSpacer(30)

    if self.widgets:
      self.container.Add(wx_util.h1(self, self.section_name), 0, wx.LEFT | wx.RIGHT, PADDING)
      self.container.AddSpacer(5)
      self.container.Add(wx_util.horizontal_rule(self), *STD_LAYOUT)
      self.container.AddSpacer(20)
      self.create_component_grid(self.container, self.widgets, cols=2)
      self.container.AddSpacer(10)

  def create_component_grid(self, parent_sizer, components, cols=2):
    for row in self.chunk(components, cols):
      hsizer = wx.BoxSizer(wx.HORIZONTAL)
      for widget in filter(None, row):
        hsizer.Add(widget.panel, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
      parent_sizer.Add(hsizer, 0, wx.EXPAND)
      parent_sizer.AddSpacer(20)

  def chunk(self, iterable, n, fillvalue=None):
    "itertools recipe: Collect data into fixed-length chunks or blocks"
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)

  def __iter__(self):
    return iter(self.widgets)


class ConfigPanel(ScrolledPanel):

  def __init__(self, parent, req_cols=1, opt_cols=3, title=None, **kwargs):
    ScrolledPanel.__init__(self, parent, **kwargs)
    self.SetupScrolling(scroll_x=False, scrollToTop=False)
    self.SetDoubleBuffered(True)

    self.title = title
    self._num_req_cols = req_cols
    self._num_opt_cols = opt_cols
    self.required_section = WidgetContainer(self, i18n._("required_args_msg"))
    self.optional_section = WidgetContainer(self, i18n._("optional_args_msg"))

    self._do_layout()
    self.Bind(wx.EVT_SIZE, self.OnResize)


  def _do_layout(self):
    STD_LAYOUT = (0, wx.LEFT | wx.RIGHT | wx.EXPAND, PADDING)

    container = wx.BoxSizer(wx.VERTICAL)
    container.AddSpacer(15)
    container.Add(self.required_section, *STD_LAYOUT)
    container.Add(self.optional_section, *STD_LAYOUT)
    self.SetSizer(container)

  def OnResize(self, evt):
    self.SetupScrolling(scroll_x=False, scrollToTop=False)
    evt.Skip()

