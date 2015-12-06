"""
Managed the internal layout for configuration options

@author: Chris
"""


import wx

from wx.lib.scrolledpanel import ScrolledPanel
from itertools import chain
from future.moves.itertools import zip_longest

from gooey.gui.util import wx_util
from gooey.gui.lang import i18n
from gooey.gui import component_builder
from gooey.gui.option_reader import OptionReader


PADDING = 10


class ConfigPanel(ScrolledPanel, OptionReader):

  def __init__(self, parent, widgets=None, req_cols=1, opt_cols=3, title=None, **kwargs):
    ScrolledPanel.__init__(self, parent, **kwargs)
    self.SetupScrolling(scroll_x=False, scrollToTop=False)

    self.SetDoubleBuffered(True)

    self.title = title

    self.widgets = component_builder.build_components(widgets)

    self._num_req_cols = req_cols
    self._num_opt_cols = opt_cols

    self._controller = None

    self._do_layout()

    self.Bind(wx.EVT_SIZE, self.OnResize)


  def _do_layout(self):
    STD_LAYOUT = (0, wx.LEFT | wx.RIGHT | wx.EXPAND, PADDING)

    container = wx.BoxSizer(wx.VERTICAL)
    container.AddSpacer(15)

    if self.title:
      container.Add(wx_util.h0(self, self.title), 0, wx.LEFT | wx.RIGHT, PADDING)
      container.AddSpacer(30)

    if self.widgets.required_args:
      container.Add(wx_util.h1(self, i18n._("required_args_msg")), 0, wx.LEFT | wx.RIGHT, PADDING)
      container.AddSpacer(5)
      container.Add(wx_util.horizontal_rule(self), *STD_LAYOUT)
      container.AddSpacer(20)

      self.CreateComponentGrid(container, self.widgets.required_args, cols=self._num_req_cols)

      container.AddSpacer(10)

    if self.widgets.optional_args:
      # container.AddSpacer(10)
      container.Add(wx_util.h1(self, i18n._("optional_args_msg")), 0, wx.LEFT | wx.RIGHT, PADDING)
      container.AddSpacer(5)
      container.Add(wx_util.horizontal_rule(self), *STD_LAYOUT)
      container.AddSpacer(20)

      self.CreateComponentGrid(container, self.widgets.optional_args, cols=self._num_opt_cols)

    self.SetSizer(container)

  def CreateComponentGrid(self, parent_sizer, components, cols=2):
    for row in self.chunk(components, cols):
      hsizer = wx.BoxSizer(wx.HORIZONTAL)
      for widget in [_f for _f in row if _f]:
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
    _f = lambda lst: [x for x in lst if x is not None]
    optional_args = _f([c.GetValue() for c in self.widgets.optional_args])
    required_args = _f([c.GetValue() for c in self.widgets.required_args if c.HasOptionString()])
    position_args = _f([c.GetValue() for c in self.widgets.required_args if not c.HasOptionString()])
    if position_args: position_args.insert(0, "--")
    return ' '.join(chain(required_args, optional_args, position_args))

  def GetRequiredArgs(self):
    return [arg.GetValue() for arg in self.widgets.required_args]

  def chunk(self, iterable, n, fillvalue=None):
    "itertools recipe: Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return zip_longest(fillvalue=fillvalue, *args)

if __name__ == '__main__':
  pass
