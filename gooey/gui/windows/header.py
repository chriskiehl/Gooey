'''
Created on Dec 23, 2013

@author: Chris
'''

import wx
from gooey.gui.pubsub import pub

from gooey.gui import imageutil, image_repository, events
from gooey.gui.util import wx_util
from gooey.gui.lang import i18n


PAD_SIZE = 10


class FrameHeader(wx.Panel):
  def __init__(self, parent=None, **kwargs):
    wx.Panel.__init__(self, parent, **kwargs)
    self.SetDoubleBuffered(True)

    self._header = None
    self._subheader = None
    self.settings_img = None
    self.running_img = None
    self.check_mark = None
    self.error_symbol = None

    self.layouts = {}

    self._init_properties()
    # self._init_components(heading, subheading)
    self._init_components()
    self._init_pages()
    self._do_layout()

    pub.subscribe(self.load_view, events.WINDOW_CHANGE)

  @property
  def title(self):
    return self._header.GetLabel()

  @title.setter
  def title(self, text):
    self._header.SetLabel(text)

  @property
  def subtitle(self):
    return self._subheader.GetLabel()

  @subtitle.setter
  def subtitle(self, text):
    self._subheader.SetLabel(text)

  def _init_properties(self):
    self.SetBackgroundColour('#ffffff')
    self.SetSize((30, 90))
    self.SetMinSize((120, 80))

  def _init_components(self):
    self._header = wx_util.h1(self, '')
    self._subheader = wx.StaticText(self, label='')

    self.settings_img = self._load_image(image_repository.config_icon, height=79)
    self.running_img = self._load_image(image_repository.running_icon, 79)
    self.check_mark = self._load_image(image_repository.success_icon, height=75)
    self.error_symbol = self._load_image(image_repository.error_icon, height=75)


  def _do_layout(self):
    vsizer = wx.BoxSizer(wx.VERTICAL)
    sizer = wx.BoxSizer(wx.HORIZONTAL)
    headings_sizer = self.build_heading_sizer()
    sizer.Add(headings_sizer, 1, wx.ALIGN_LEFT | wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND | wx.LEFT, PAD_SIZE)
    sizer.Add(self.settings_img, 0, wx.ALIGN_RIGHT | wx.EXPAND | wx.RIGHT, PAD_SIZE)
    sizer.Add(self.running_img, 0, wx.ALIGN_RIGHT | wx.EXPAND | wx.RIGHT, PAD_SIZE)
    sizer.Add(self.check_mark, 0, wx.ALIGN_RIGHT | wx.EXPAND | wx.RIGHT, PAD_SIZE)
    sizer.Add(self.error_symbol, 0, wx.ALIGN_RIGHT | wx.EXPAND | wx.RIGHT, PAD_SIZE)
    self.running_img.Hide()
    self.check_mark.Hide()
    self.error_symbol.Hide()
    vsizer.Add(sizer, 1, wx.EXPAND)
    self.SetSizer(vsizer)

  def _load_image(self, img_path, height=70):
    return imageutil.resize_bitmap(self, imageutil._load_image(img_path), height)

  def build_heading_sizer(self):
    sizer = wx.BoxSizer(wx.VERTICAL)
    sizer.AddStretchSpacer(1)
    sizer.Add(self._header, 0)
    sizer.Add(self._subheader, 0)
    sizer.AddStretchSpacer(1)
    return sizer

  def _init_pages(self):

    def config():
      self._header.SetLabel(self.heading_msg)
      self._subheader.SetLabel(self.subheading_msg)
      self.settings_img.Show()
      self.check_mark.Hide()
      self.running_img.Hide()
      self.error_symbol.Hide()
      self.Layout()

    def running():
      self._header.SetLabel(i18n._("running_title"))
      self._subheader.SetLabel(i18n._('running_msg'))
      self.check_mark.Hide()
      self.settings_img.Hide()
      self.running_img.Show()
      self.error_symbol.Hide()
      self.Layout()

    def success():
      self._header.SetLabel(i18n._('finished_title'))
      self._subheader.SetLabel(i18n._('finished_msg'))
      self.running_img.Hide()
      self.check_mark.Show()
      self.Layout()

    def error():
      self._header.SetLabel(i18n._('finished_title'))
      self._subheader.SetLabel(i18n._('finished_error'))
      self.running_img.Hide()
      self.error_symbol.Show()
      self.Layout()

    self.layouts = locals()

  def load_view(self, view_name=None):
    self.layouts.get(view_name, lambda: None)()

