"""
Created on Dec 28, 2013

@author: Chris
"""

import wx
from wx.lib.scrolledpanel import ScrolledPanel

from gooey.gui.component_factory import ComponentFactory
from gooey.gui.option_reader import OptionReader
import styling


PADDING = 10


class AdvancedConfigPanel(ScrolledPanel, OptionReader):
  """
  Abstract class for the Footer panels.
  """

  def __init__(self, parent, action_groups=None, **kwargs):
    ScrolledPanel.__init__(self, parent, **kwargs)
    self.SetupScrolling()

    self._action_groups = action_groups
    self._positionals = len(action_groups._positionals) > 0
    self.components = ComponentFactory(action_groups)

    self._msg_req_args = None
    self._msg_opt_args = None

    self._controller = None

    self._init_components()
    self._do_layout()
    self.Bind(wx.EVT_SIZE, self.OnResize)


  def _init_components(self):
    self._msg_req_args = (styling.H1(self, "Required Arguments")
                          if self._positionals else None)
    self._msg_opt_args = styling.H1(self, "Optional Arguments")

  def _do_layout(self):
    STD_LAYOUT = (0, wx.LEFT | wx.RIGHT | wx.EXPAND, PADDING)

    container = wx.BoxSizer(wx.VERTICAL)
    container.AddSpacer(15)

    if self._positionals:
      container.Add(self._msg_req_args, 0, wx.LEFT | wx.RIGHT, PADDING)
      container.AddSpacer(5)
      container.Add(styling.HorizontalRule(self), *STD_LAYOUT)
      container.AddSpacer(20)

      self.AddWidgets(container, self.components.required_args, add_space=True)

      container.AddSpacer(10)

    container.AddSpacer(10)
    container.Add(self._msg_opt_args, 0, wx.LEFT | wx.RIGHT, PADDING)
    container.AddSpacer(5)
    container.Add(styling.HorizontalRule(self), *STD_LAYOUT)
    container.AddSpacer(20)

    flag_grids = self.CreateComponentGrid(self.components.flags, cols=3, vgap=15)
    general_opts_grid = self.CreateComponentGrid(self.components.general_options)
    container.Add(general_opts_grid, *STD_LAYOUT)
    container.AddSpacer(30)
    container.Add(flag_grids, *STD_LAYOUT)

    self.SetSizer(container)

  def AddWidgets(self, sizer, components, add_space=False, padding=PADDING):
    for component in components:
      widget_group = component.Build(parent=self)
      sizer.Add(widget_group, 0, wx.LEFT | wx.RIGHT | wx.EXPAND, padding)
      if add_space:
        sizer.AddSpacer(8)

  def CreateComponentGrid(self, components, cols=2, vgap=10):
    gridsizer = wx.GridSizer(rows=0, cols=cols, vgap=vgap, hgap=4)
    self.AddWidgets(gridsizer, components)
    return gridsizer

  def OnResize(self, evt):
    for component in self.components:
      component.Update(evt.m_size)
    evt.Skip()

  def RegisterController(self, controller):
    if self._controller is None:
      self._controller = controller

  def GetOptions(self):
    """
    returns the collective values from all of the
    widgets contained in the panel"""
    values = [c.GetValue()
              for c in self.components
              if c.GetValue() is not None]
    return ' '.join(values)


if __name__ == '__main__':
  pass
