'''
Created on Jan 19, 2014
@author: Chris
'''

import sys

import wx

from gooey.gui import image_repository, events
from gooey.gui.lang.i18n import _
from gooey.gui.pubsub import pub
from gooey.gui.util import wx_util
from gooey.gui.windows import footer, header, layouts
from gooey.gui.windows.runtime_display_panel import RuntimeDisplay

YES = 5103
NO = 5104

class BaseWindow(wx.Frame):
  '''
  Primary Frame under which all sub-Panels are organized.
  '''

  def __init__(self, layout_type):
    wx.Frame.__init__(self, parent=None, id=-1)

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

  @property
  def progress_bar(self):
    return self.foot_panel.progress_bar

  def set_display_font_style(self, style):
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

  def _init_components(self):
    self.runtime_display = RuntimeDisplay(self)
    self.head_panel = header.FrameHeader(parent=self)
    self.foot_panel = footer.Footer(self)
    self.panels = [self.head_panel, self.config_panel, self.foot_panel]

  def _do_layout(self):
    sizer = wx.BoxSizer(wx.VERTICAL)
    sizer.Add(self.head_panel, 0, wx.EXPAND)
    sizer.Add(wx_util.horizontal_rule(self), 0, wx.EXPAND)

    if self.layout_type == layouts.COLUMN:
      self.config_panel = layouts.ColumnLayout(self)
    else:
      self.config_panel = layouts.FlatLayout(self)

    sizer.Add(self.config_panel, 1, wx.EXPAND)

    sizer.Add(self.runtime_display, 1, wx.EXPAND)

    self.runtime_display.Hide()
    sizer.Add(wx_util.horizontal_rule(self), 0, wx.EXPAND)
    sizer.Add(self.foot_panel, 0, wx.EXPAND)
    self.SetSizer(sizer)

    self.sizer = sizer

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

  def hide_all_buttons(self):
    self.foot_panel.hide_all_buttons()

  def update_console_async(self, msg):
    wx.CallAfter(self.runtime_display.append_text, msg)

  def update_progress_aync(self, progress):
    wx.CallAfter(self.UpdateProgressBar, progress)

  def onResize(self, evt):
    evt.Skip()

  def onClose(self, evt):
    if evt.CanVeto():
      evt.Veto()
    pub.send_message(str(events.WINDOW_CLOSE))

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

  def show_missing_args_dialog(self):
    self.show_dialog(_('error_title'), _('error_required_fields'), wx.ICON_ERROR)

  def confirm_exit_dialog(self):
    result = self.show_dialog(_('sure_you_want_to_exit'), _('close_program'), wx.YES_NO)
    return result == YES

  def confirm_stop_dialog(self):
    result = self.show_dialog(_('sure_you_want_to_stop'), _('stop_task'), wx.YES_NO)
    return result == YES

if __name__ == '__main__':
  pass
