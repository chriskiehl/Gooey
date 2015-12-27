'''
Created on Jan 19, 2014
@author: Chris
'''

import sys
from distutils import config

import wx
from gooey.gui.pubsub import pub

from gooey.gui.lang import i18n
from gooey.gui.windows.advanced_config import ConfigPanel
from gooey.gui.windows.runtime_display_panel import RuntimeDisplay
from gooey.gui import image_repository, events
from gooey.gui.util import wx_util
from gooey.gui.windows import footer, header, layouts


class BaseWindow(wx.Frame):
  def __init__(self, build_spec, layout_type):
    wx.Frame.__init__(self, parent=None, id=-1)

    self.build_spec = build_spec

    self.SetDoubleBuffered(True)

    # type of gui to render
    self.layout_type = layout_type

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
    self.Bind(wx.EVT_SIZE, self.onResize)
    self.Bind(wx.EVT_CLOSE, self.onClose)


  @property
  def window_size(self):
    return self.GetSize()

  @window_size.setter
  def window_size(self, size_tuple):
    self.SetSize(size_tuple)

  @property
  def window_title(self):
    return self.GetTitle()

  @window_title.setter
  def window_title(self, title):
    self.SetTitle(title)

  @property
  def heading_title(self):
    return self.head_panel.title

  @heading_title.setter
  def heading_title(self, text):
    self.head_panel.title = text

  @property
  def heading_subtitle(self):
    return self.head_panel.subtitle

  @heading_subtitle.setter
  def heading_subtitle(self, text):
    self.head_panel.subtitle = text

  @property
  def required_section(self):
    return self.config_panel.main_content.required_section

  @property
  def optional_section(self):
    return self.config_panel.main_content.optional_section


  def set_display_font_style(self, style):
    '''
    wx.FONTFAMILY_DEFAULT	Chooses a default font.
    wx.FONTFAMILY_DECORATIVE	A decorative font.
    wx.FONTFAMILY_ROMAN	A formal, serif font.
    wx.FONTFAMILY_SCRIPT	A handwriting font.
    wx.FONTFAMILY_SWISS	A sans-serif font.
    wx.FONTFAMILY_MODERN	Usually a fixed pitch font.
    wx.FONTFAMILY_TELETYPE	A teletype font.
    '''
    # TODO: make this not stupid
    # TODO: _actual_ font support
    self.runtime_display.set_font_style(
      wx.MODERN if style == 'monospace' else wx.DEFAULT)



  def _init_properties(self):
    # self.SetTitle(self.build_spec['program_name'])
    # self.SetSize(self.build_spec['default_size'])
    # # self.SetMinSize((400, 300))
    self.icon = wx.Icon(image_repository.program_icon, wx.BITMAP_TYPE_ICO)
    self.SetIcon(self.icon)

  def enable_stop_button(self):
    self.foot_panel.stop_button.Enable()

  def disable_stop_button(self):
    self.foot_panel.stop_button.Disable()

  def show(self, *args):
    '''
    Looks up the attribute across all available
    panels and calls `Show()`
    '''
    self._set_visibility('Show', *args)

  def hide(self, *args):
    '''
    Looks up the attribute across all available
    panels and calls `Show()`
    '''
    self._set_visibility('Hide', *args)

  def _set_visibility(self, action, *args):
    '''
    Checks for the existence `attr` on a given `panel` and
    performs `action` if found
    '''
    def _set_visibility(obj, attrs):
      for attr in attrs:
        if hasattr(obj, attr):
          instance = getattr(obj, attr)
          getattr(instance, action)()
          instance.Layout()
    for panel in [self, self.head_panel, self.foot_panel, self.config_panel]:
      _set_visibility(panel, args)


  def _init_components(self):
    # init gui
    # _desc = self.build_spec['program_description']
    # self.head_panel = header.FrameHeader(
    #     heading=i18n._("settings_title"),
    #     subheading=_desc or '',
    #     parent=self)
    self.runtime_display = RuntimeDisplay(self)
    self.head_panel = header.FrameHeader(parent=self)
    self.foot_panel = footer.Footer(self)

    # if self.build_spec['disable_stop_button']:
    #   self.foot_panel.stop_button.Disable()
    # else:
    #   self.foot_panel.stop_button.Enable()

    self.panels = [self.head_panel, self.config_panel, self.foot_panel]

  def _do_layout(self):
    sizer = wx.BoxSizer(wx.VERTICAL)
    sizer.Add(self.head_panel, 0, wx.EXPAND)
    sizer.Add(wx_util.horizontal_rule(self), 0, wx.EXPAND)

    if self.layout_type == layouts.COLUMN:
      self.config_panel = layouts.ColumnLayout(self)
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

  def onResize(self, evt):
    evt.Skip()

  def onClose(self, evt):
    if evt.CanVeto():
      evt.Veto()
    pub.send_message(str(events.WINDOW_CLOSE))

  def PublishConsoleMsg(self, text):
    self.runtime_display.append_text(text)

  def UpdateProgressBar(self, value):
    pb = self.foot_panel.progress_bar
    if value < 0:
      pb.Pulse()
    else:
      value = min(int(value), pb.GetRange())
      if pb.GetValue() != value:
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

  def show_dialog(self, title, content, style):
    dlg = wx.MessageDialog(None, content, title, style)
    result = dlg.ShowModal()
    dlg.Destroy()
    return result


if __name__ == '__main__':
  pass
