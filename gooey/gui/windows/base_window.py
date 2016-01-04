'''
Created on Jan 19, 2014
@author: Chris
'''

import sys

import wx
from gooey.gui.pubsub import pub

from gooey.gui.controller import Controller
from gooey.gui.lang import i18n
from gooey.gui.windows.advanced_config import ConfigPanel
from gooey.gui.windows.runtime_display_panel import RuntimeDisplay
from gooey.gui import image_repository, events
from gooey.gui.util import wx_util
from gooey.gui.windows import footer, header, layouts


class BaseWindow(wx.Frame):
  def __init__(self, build_spec):
    wx.Frame.__init__(self, parent=None, id=-1)

    self.build_spec = build_spec

    self._controller = None

    self.SetDoubleBuffered(True)

    # Components
    self.icon = None
    self.head_panel = None
    self.config_panel = None
    self.runtime_display = None
    self.foot_panel = None
    self.panels = None

    self._init_properties()
    self._init_components()
    self._do_layout()
    self._init_pages()
    self._init_controller()
    self.registerControllers()
    self.Bind(wx.EVT_SIZE, self.onResize)
    self.Bind(wx.EVT_CLOSE, self.onClose)

  def _init_properties(self):
    self.SetTitle(self.build_spec['program_name'])
    self.SetSize(self.build_spec['default_size'])
    # self.SetMinSize((400, 300))
    self.icon = wx.Icon(image_repository.program_icon, wx.BITMAP_TYPE_ICO)
    self.SetIcon(self.icon)

  def _init_components(self):
    # init gui
    _desc = self.build_spec['program_description']
    self.head_panel = header.FrameHeader(
        heading=i18n._("settings_title"),
        subheading=_desc or '',
        parent=self)

    self.runtime_display = RuntimeDisplay(self, self.build_spec)
    self.foot_panel = footer.Footer(self)

    if self.build_spec['disable_stop_button']:
      self.foot_panel.stop_button.Disable()
    else:
      self.foot_panel.stop_button.Enable()

    self.panels = [self.head_panel, self.config_panel, self.foot_panel]

  def _do_layout(self):
    sizer = wx.BoxSizer(wx.VERTICAL)
    sizer.Add(self.head_panel, 0, wx.EXPAND)
    sizer.Add(wx_util.horizontal_rule(self), 0, wx.EXPAND)

    if self.build_spec['layout_type'] == 'column':
      self.config_panel = layouts.ColumnLayout(self, build_spec=self.build_spec)
      sizer.Add(self.config_panel, 1, wx.EXPAND)
    else:
      self.config_panel = layouts.FlatLayout(self, build_spec=self.build_spec)
      sizer.Add(self.config_panel, 1, wx.EXPAND)

    sizer.Add(self.runtime_display, 1, wx.EXPAND)

    self.runtime_display.Hide()
    sizer.Add(wx_util.horizontal_rule(self), 0, wx.EXPAND)
    sizer.Add(self.foot_panel, 0, wx.EXPAND)
    self.SetSizer(sizer)

    self.sizer = sizer

    pub.subscribe(self.myListener, "panelListener")
    pub.subscribe(self.load_view, events.WINDOW_CHANGE)



  def myListener(self, message):
    if message == 'fetch':
      del self.config_panel

  def _init_controller(self):
    self._controller = Controller(base_frame=self, build_spec=self.build_spec)

  def registerControllers(self):
    for panel in self.panels:
      pass

  def GetOptions(self):
    return self.config_panel.GetOptions()

  def GetRequiredArgs(self):
    return self.config_panel.GetRequiredArgs()

  def GetOptionalArgs(self):
    return self.config_panel.GetOptionalArgs()


  def _init_pages(self):

    def config():
      self.config_panel.Show()
      self.runtime_display.Hide()

    def running():
      self.config_panel.Hide()
      self.runtime_display.Show()
      self.Layout()

    def success():
      running()

    def error():
      running()

    self.layouts = locals()

  def load_view(self, view_name=None):
    self.layouts.get(view_name, lambda: None)()

  def ManualStart(self):
    self._controller.manual_restart()

  def onResize(self, evt):
    evt.Skip()

  def onClose(self, evt):
    if evt.CanVeto():
      evt.Veto()
    pub.send_message(str(events.WINDOW_CLOSE))

  def PublishConsoleMsg(self, text):
    self.runtime_display.cmd_textbox.AppendText(text)

  def UpdateProgressBar(self, value):
    pb = self.foot_panel.progress_bar
    if value < 0:
      pb.Pulse()
    else:
      value = min(int(value), pb.GetRange())
      if pb.GetValue() != value or value == 0:
        # Windows 7 progress bar animation hack
        # http://stackoverflow.com/questions/5332616/disabling-net-progressbar-animation-when-changing-value
        if self.build_spec["disable_progress_bar_animation"] \
           and sys.platform.startswith("win"):
          if pb.GetRange() == value:
            pb.SetValue(value)
            pb.SetValue(value-1)
          else:
            pb.SetValue(value+1)
        pb.SetValue(value)


if __name__ == '__main__':
  pass
