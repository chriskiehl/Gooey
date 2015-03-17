"""
Created on Dec 28, 2013

@author: Chris
"""
from itertools import chain

import wx
from wx.lib.scrolledpanel import ScrolledPanel

from gooey.gui import component_builder
from gooey.gui.lang import i18n
from gooey.gui.option_reader import OptionReader
from gooey.gui import styling

PADDING = 10

class AdvancedConfigPanel(ScrolledPanel, OptionReader):
  """
  Abstract class for the Footer panels.
  """

  def __init__(self, parent, build_spec=None, **kwargs):
    ScrolledPanel.__init__(self, parent, **kwargs)
    self.SetupScrolling(scroll_x=False, scrollToTop=False)

    self.SetDoubleBuffered(True)

    self._action_groups = build_spec
    self._positionals = build_spec.get('required', None)
    self.components = component_builder.ComponentBuilder(build_spec)

    self._msg_req_args = None
    self._msg_opt_args = None

    self._controller = None

    self._init_components()
    self._do_layout()
    self.Bind(wx.EVT_SIZE, self.OnResize)


  def _init_components(self):
    self._msg_req_args = (styling.H1(self, i18n.translate("required_args_msg"))
                          if self._positionals else None)
    self._msg_opt_args = styling.H1(self, i18n.translate("optional_args_msg"))

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

    self.CreateComponentGrid(container, self.components.general_options, cols=2)
    self.CreateComponentGrid(container, self.components.flags, cols=3)
    # container.Add(general_opts_grid, *STD_LAYOUT)
    # container.AddSpacer(30)
    # container.Add(flag_grids, 0, wx.LEFT | wx.RIGHT | wx.EXPAND, PADDING)

    self.SetSizer(container)

  def AddWidgets(self, sizer, components, add_space=False, padding=PADDING):
    for component in components:
      widget_group = component.build(parent=self)
      sizer.Add(widget_group, 0, wx.LEFT | wx.RIGHT | wx.EXPAND, padding)
      if add_space:
        sizer.AddSpacer(8)

  def CreateComponentGrid(self, parent_sizer, components, cols=2):
    rows = [components[i:i+cols] for i in range(0, len(components), cols)]
    for row in rows:
      hsizer = wx.BoxSizer(wx.HORIZONTAL)
      for widget in row:
        hsizer.Add(widget.build(self), 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
      # hsizer.FitInside(parent_sizer)
      parent_sizer.Add(hsizer, 0, wx.EXPAND)
      parent_sizer.AddSpacer(20)

  def OnResize(self, evt):
    self.Freeze()
    for component in self.components:
      component.onResize(evt)
    self.SetupScrolling(scroll_x=False, scrollToTop=False)
    evt.Skip()
    self.Thaw()

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

  def GetRequiredArgs(self):
    if not self.components.required_args:
        return None
    else:
        return [arg.GetValue() for arg in self.components.required_args]

  def GetOptionalArgs(self):
    if not self.components.general_args:
        return None
    else:
        return [arg.GetValue() for arg in
            chain(self.components.general_options, self.components.flags)]


if __name__ == '__main__':
  pass
