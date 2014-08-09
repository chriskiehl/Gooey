'''
Created on Dec 23, 2013

@author: Chris
'''

import itertools

import wx
from gooey import i18n
from gooey.gui import imageutil
from gooey import image_repository


PAD_SIZE = 10


class FrameHeader(wx.Panel):
  def __init__(self, heading, subheading, **kwargs):

    wx.Panel.__init__(self, **kwargs)

    self._controller = None

    self._init_properties()
    self._init_components(heading, subheading)
    self._init_pages()
    self._do_layout()


  def _init_properties(self):
    self.SetBackgroundColour('#ffffff')
    self.SetSize((30, 90))
    self.SetMinSize((120, 80))

  def _init_components(self, heading, subheading):
    self._header = self._bold_static_text(heading)
    self._subheader = wx.StaticText(self, label=subheading)
    self._settings_img = self._load_image(image_repository.settings2, height=79)
    self._running_img = self._load_image(image_repository.computer3, 79)
    self._check_mark = self._load_image(image_repository.alessandro_rei_checkmark, height=75)


  def _do_layout(self):
    vsizer = wx.BoxSizer(wx.VERTICAL)
    sizer = wx.BoxSizer(wx.HORIZONTAL)
    headings_sizer = self.build_heading_sizer()
    sizer.Add(headings_sizer, 1, wx.ALIGN_LEFT | wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND | wx.LEFT, PAD_SIZE)
    sizer.Add(self._settings_img, 0, wx.ALIGN_RIGHT | wx.EXPAND | wx.RIGHT, PAD_SIZE)
    sizer.Add(self._running_img, 0, wx.ALIGN_RIGHT | wx.EXPAND | wx.RIGHT, PAD_SIZE)
    sizer.Add(self._check_mark, 0, wx.ALIGN_RIGHT | wx.EXPAND | wx.RIGHT, PAD_SIZE)
    self._running_img.Hide()
    self._check_mark.Hide()
    vsizer.Add(sizer, 1, wx.EXPAND)
    self.SetSizer(vsizer)

  def _bold_static_text(self, label):
    txt = wx.StaticText(self, label=label)
    font_size = txt.GetFont().GetPointSize()
    txt.SetFont(wx.Font(font_size * 1.2, wx.FONTFAMILY_DEFAULT,
                        wx.FONTWEIGHT_NORMAL, wx.FONTWEIGHT_BOLD, False)
    )
    return txt

  def _load_image(self, img_path, height=70):
    return imageutil.resize_bitmap(self,
                                    imageutil._load_image(img_path),
                                    height)

  def build_heading_sizer(self):
    sizer = wx.BoxSizer(wx.VERTICAL)
    sizer.AddStretchSpacer(1)
    sizer.Add(self._header, 0)
    sizer.Add(self._subheader, 0)
    sizer.AddStretchSpacer(1)
    return sizer

  def RegisterController(self, controller):
    if self._controller is None:
      self._controller = controller

  def _init_pages(self):
    messages = [[
                  i18n.translate("running_title"),
                  i18n.translate('running_msg')
                ], [
                  i18n.translate('finished_title'),
                  i18n.translate('finished_msg')
                ]]
    pages = [[
               self._header.SetLabel,
               self._subheader.SetLabel,
               self._settings_img.Hide,
               self._running_img.Show,
               self.Layout,
             ], [
               self._header.SetLabel,
               self._subheader.SetLabel,
               self._running_img.Hide,
               self._check_mark.Show,
               self.Layout,
             ]]
    self._messages = iter(messages)
    self._pages = iter(pages)

  def NextPage(self):
    messages = next(self._messages)
    commands = next(self._pages)

    _zipl = itertools.izip_longest

    for func, arg in _zipl(commands, messages, fillvalue=None):
      func(arg) if arg else func()