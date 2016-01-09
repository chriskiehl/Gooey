'''
Created on Dec 23, 2013

@author: Chris
'''

import wx
import wx.animate

from gooey.gui.pubsub import pub

from gooey.gui.lang import i18n
from gooey.gui import imageutil, events


class Footer(wx.Panel):
  '''
  Footer section used on the configuration
  screen of the application

  args:
    parent: wxPython parent windows
    controller: controller class used in delagating all the commands
  '''

  def __init__(self, parent, **kwargs):
    wx.Panel.__init__(self, parent, **kwargs)
    self.SetMinSize((30, 53))

    # components
    self.cancel_button = None
    self.start_button = None
    self.progress_bar = None
    self.close_button = None
    self.stop_button = None
    self.restart_button = None
    self.buttons = None

    self.layouts = {}

    self._init_components()
    self._do_layout()

    for button in self.buttons:
      self.Bind(wx.EVT_BUTTON, self.dispatch_click, button)


  def _init_components(self):
    self.cancel_button      = self.button(i18n._('cancel'),  wx.ID_CANCEL,  event_id=int(events.WINDOW_CANCEL))
    self.stop_button        = self.button(i18n._('stop'),    wx.ID_OK,      event_id=int(events.WINDOW_STOP))
    self.start_button       = self.button(i18n._('start'),   wx.ID_OK,      event_id=int(events.WINDOW_START))
    self.close_button       = self.button(i18n._("close"),   wx.ID_OK,      event_id=int(events.WINDOW_CLOSE))
    self.restart_button     = self.button(i18n._('restart'), wx.ID_OK,      event_id=int(events.WINDOW_RESTART))
    self.edit_button        = self.button(i18n._('edit'),    wx.ID_OK,      event_id=int(events.WINDOW_EDIT))

    self.progress_bar  = wx.Gauge(self, range=100)

    self.buttons = [self.cancel_button, self.start_button,
                    self.stop_button, self.close_button,
                    self.restart_button, self.edit_button]

  def _do_layout(self):
    self.stop_button.Hide()
    self.restart_button.Hide()

    v_sizer = wx.BoxSizer(wx.VERTICAL)
    h_sizer = wx.BoxSizer(wx.HORIZONTAL)

    h_sizer.Add(self.progress_bar, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 20)
    self.progress_bar.Hide()

    h_sizer.AddStretchSpacer(1)
    h_sizer.Add(self.cancel_button, 0, wx.ALIGN_RIGHT | wx.RIGHT, 20)
    h_sizer.Add(self.start_button, 0, wx.ALIGN_RIGHT | wx.RIGHT, 20)
    h_sizer.Add(self.stop_button, 0, wx.ALIGN_RIGHT | wx.RIGHT, 20)

    v_sizer.AddStretchSpacer(1)
    v_sizer.Add(h_sizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND)

    h_sizer.Add(self.edit_button, 0, wx.ALIGN_RIGHT | wx.RIGHT, 10)
    h_sizer.Add(self.restart_button, 0, wx.ALIGN_RIGHT | wx.RIGHT, 10)
    h_sizer.Add(self.close_button, 0, wx.ALIGN_RIGHT | wx.RIGHT, 20)
    self.edit_button.Hide()
    self.restart_button.Hide()
    self.close_button.Hide()

    v_sizer.AddStretchSpacer(1)
    self.SetSizer(v_sizer)

  def button(self, label=None, style=None, event_id=-1):
    return wx.Button(
      parent=self,
      id=event_id,
      size=(90, 24),
      label=label,
      style=style)

  def dispatch_click(self, event):
    pub.send_message(str(event.GetId()))
    event.Skip()

  def hide_all_buttons(self):
    for button in self.buttons:
      button.Hide()

  def _load_image(self, img_path, height=70):
    return imageutil.resize_bitmap(self, imageutil._load_image(img_path), height)






