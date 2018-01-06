"""
Managed the internal layout for configuration options

@author: Chris
"""


import wx
from wx.lib.scrolledpanel import ScrolledPanel
from itertools import chain
try:
    from itertools import zip_longest
except ImportError:
    from itertools import izip_longest as zip_longest
from collections import OrderedDict

from gooey.gui.util import wx_util
from gooey.gui.lang import i18n
from gooey.gui.widgets import components

PADDING = 10


class WidgetContainer(ScrolledPanel):
  '''
  Collection of widgets
  '''
  def __init__(self, parent, section_name, use_tabs, *args, **kwargs):
    if use_tabs:
      ScrolledPanel.__init__(self, parent, *args, **kwargs)
      self.SetupScrolling(scroll_x=False, scrollToTop=False)
    else:
      wx.Panel.__init__(self, parent, *args, **kwargs)

    self.use_tabs = use_tabs
    self.section_name = section_name
    self.title = None
    self.widgets = []

    self.container = wx.BoxSizer(wx.VERTICAL)
    self.SetSizer(self.container)

  def layout(self, num_columns):
    STD_LAYOUT = (0, wx.LEFT | wx.RIGHT | wx.EXPAND, PADDING)

    if self.title:
      self.container.Add(wx_util.h0(self, self.title), 0, wx.LEFT | wx.RIGHT, PADDING)
      self.container.AddSpacer(30)

    if self.widgets:
      if not self.use_tabs:
        self.container.Add(wx_util.h1(self, self.section_name), 0, wx.LEFT | wx.RIGHT, PADDING)
        self.container.AddSpacer(5)
      self.container.Add(wx_util.horizontal_rule(self), *STD_LAYOUT)
      self.container.AddSpacer(20)
      self.create_component_grid(self.container, self.widgets, cols=num_columns)
      self.container.AddSpacer(10)

  def populate(self, widgets, num_columns):
    for index, widget in enumerate(widgets):
      widget_class = getattr(components, widget.type)
      widget_instance = widget_class(self, widget.title, widget.help, widget.choices)
      widget.widget_instance = widget_instance
      self.widgets.append(widget_instance)
    self.layout(num_columns)

  def get_values(self):
    return [x.get_value() for x in self.widgets]

  def clear(self):
    self.container.Clear(True)
    self.widgets = []

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
    return zip_longest(fillvalue=fillvalue, *args)

  def __iter__(self):
    return iter(self.widgets)


class ConfigPanel(ScrolledPanel):

  def __init__(self, parent, req_cols=1, opt_cols=3, title=None, use_tabs=True, **kwargs):
    super(ConfigPanel, self).__init__(parent, **kwargs)
    if use_tabs:
      self.nb = wx.Notebook(self, **kwargs)
    else:
      self.SetupScrolling(scroll_x=False, scrollToTop=False)

    self.SetDoubleBuffered(True)

    self.title = title
    self._num_req_cols = req_cols
    self._num_opt_cols = opt_cols
    self.use_tabs = use_tabs

    self.section = OrderedDict()
    self.Bind(wx.EVT_SIZE, self.OnResize)

  def CreateSection(self, name):
    if self.use_tabs:
      self.section[name] = WidgetContainer(self.nb, i18n._(name), self.use_tabs)
      self.nb.AddPage(self.section[name], name)
    else:
      self.section[name] = WidgetContainer(self, i18n._(name), self.use_tabs)

  def DeleteSection(self, name):
    del self.section[name]
    if self.use_tabs:
      for index in range(self.nb.GetPageCount()):
        if self.nb.GetPageText(index) == name:
          self.nb.DeletePage(index)
          break

  def Section(self, name):
    return self.section[name]

  def _do_layout(self):
    STD_LAYOUT = (1 if self.use_tabs else 0, wx.LEFT | wx.RIGHT | wx.EXPAND, PADDING)

    if self.use_tabs:
      container = wx.BoxSizer(wx.VERTICAL)
      container.AddSpacer(15)
      container.Add(self.nb, *STD_LAYOUT)
    else:
      container = wx.BoxSizer(wx.VERTICAL)
      container.AddSpacer(15)
      for section in self.section.keys():
        container.Add(self.section[section], *STD_LAYOUT)
    self.SetSizer(container)

  def OnResize(self, evt):
    if not self.use_tabs:
      self.SetupScrolling(scroll_x=False, scrollToTop=False)
    evt.Skip()

  def clear(self):
    for section in self.section.keys():
      self.section[section].clear()

