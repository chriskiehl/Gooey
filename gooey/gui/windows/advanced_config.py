"""
Managed the internal layout for configuration options

@author: Chris
"""

import itertools
from itertools import chain

import wx
from wx.lib.scrolledpanel import ScrolledPanel

from gooey.gui.util import wx_util
from gooey.gui.lang import i18n
from gooey.gui import component_builder
from gooey.gui.option_reader import OptionReader

PADDING = 10


class AdvancedConfigPanel(ScrolledPanel, OptionReader):

  def __init__(self, parent, build_spec=None, **kwargs):
    ScrolledPanel.__init__(self, parent, **kwargs)
    self.SetupScrolling(scroll_x=False, scrollToTop=False)

    self.SetDoubleBuffered(True)

    self._build_spec = build_spec
    self.widgets = component_builder.build_components(build_spec['widgets'])

    self._msg_req_args = None
    self._msg_opt_args = None

    self._controller = None

    self._do_layout()

    self.Bind(wx.EVT_SIZE, self.OnResize)


  def _do_layout(self):
    STD_LAYOUT = (0, wx.LEFT | wx.RIGHT | wx.EXPAND, PADDING)

    container = wx.BoxSizer(wx.VERTICAL)
    container.AddSpacer(15)

    if self.widgets.required_args:
      container.Add(wx_util.H1(self, i18n.translate("required_args_msg")), 0, wx.LEFT | wx.RIGHT, PADDING)
      container.AddSpacer(5)
      container.Add(wx_util.HorizontalRule(self), *STD_LAYOUT)
      container.AddSpacer(20)

      self.CreateComponentGrid(container, self.widgets.required_args, cols=self._build_spec['requireds_cols'])

      container.AddSpacer(10)


    if self.widgets.optional_args:
      container.AddSpacer(10)
      container.Add(wx_util.H1(self, i18n.translate("optional_args_msg")), 0, wx.LEFT | wx.RIGHT, PADDING)
      container.AddSpacer(5)
      container.Add(wx_util.HorizontalRule(self), *STD_LAYOUT)
      container.AddSpacer(20)

      self.CreateComponentGrid(container, self.widgets.optional_args, cols=self._build_spec['optionals_cols'])

    self.SetSizer(container)

  def CreateComponentGrid(self, parent_sizer, components, cols=2):
    for row in self.chunk(components, cols):
      hsizer = wx.BoxSizer(wx.HORIZONTAL)
      for widget in filter(None, row):
        hsizer.Add(widget.build(self), 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
      # hsizer.FitInside(parent_sizer)
      parent_sizer.Add(hsizer, 0, wx.EXPAND)
      parent_sizer.AddSpacer(20)

  def OnResize(self, evt):
    self.SetupScrolling(scroll_x=False, scrollToTop=False)
    evt.Skip()

  def RegisterController(self, controller):
    if self._controller is None:
      self._controller = controller

  def GetOptions(self):
    """
    returns the collective values from all of the
    widgets contained in the panel"""
    values = [c.GetValue()
              for c in chain(*self.widgets)
              if c.GetValue() is not None]
    return ' '.join(values)

  def GetRequiredArgs(self):
    return [arg.GetValue() for arg in self.widgets.required_args]

  def chunk(self, iterable, n, fillvalue=None):
    "itertools recipe: Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return itertools.izip_longest(fillvalue=fillvalue, *args)

if __name__ == '__main__':
  pass
