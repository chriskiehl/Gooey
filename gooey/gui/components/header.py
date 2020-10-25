'''
Created on Dec 23, 2013

@author: Chris
'''

import wx

from gooey.gui import imageutil, image_repository
from gooey.gui.util import wx_util
from gooey.gui.three_to_four import bitmapFromImage
from gooey.util.functional import getin
from gooey.gui.components.mouse import notifyMouseEvent

PAD_SIZE = 10


class FrameHeader(wx.Panel):
    def __init__(self, parent, buildSpec, **kwargs):
        wx.Panel.__init__(self, parent, **kwargs)
        self.SetDoubleBuffered(True)

        self.buildSpec = buildSpec

        self._header = None
        self._subheader = None
        self.settings_img = None
        self.running_img = None
        self.check_mark = None
        self.error_symbol = None

        self.images = []

        self.layoutComponent()
        self.bindMouseEvents()



    def setTitle(self, title):
        self._header.SetLabel(title)

    def setSubtitle(self, subtitle):
        self._subheader.SetLabel(subtitle)

    def setImage(self, image):
        for img in self.images:
            img.Show(False)
        getattr(self, image).Show(True)
        self.Layout()

    def layoutComponent(self):
        self.SetBackgroundColour(self.buildSpec['header_bg_color'])
        self.SetSize((30, self.buildSpec['header_height']))
        self.SetMinSize((120, self.buildSpec['header_height']))

        self._header = wx_util.h1(self, label=self.buildSpec['program_name'])
        self._subheader = wx.StaticText(self, label=self.buildSpec['program_description'])

        images = self.buildSpec['images']
        targetHeight = self.buildSpec['header_height'] - 10
        self.settings_img = self._load_image(images['configIcon'], targetHeight)
        self.running_img = self._load_image(images['runningIcon'], targetHeight)
        self.check_mark = self._load_image(images['successIcon'], targetHeight)
        self.error_symbol = self._load_image(images['errorIcon'], targetHeight)

        self.images = [
            self.settings_img,
            self.running_img,
            self.check_mark,
            self.error_symbol
        ]

        vsizer = wx.BoxSizer(wx.VERTICAL)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        headings_sizer = self.build_heading_sizer()
        sizer.Add(headings_sizer, 1,
                  wx.ALIGN_LEFT | wx.EXPAND | wx.LEFT,
                  PAD_SIZE)
        sizer.Add(self.settings_img, 0, wx.EXPAND | wx.RIGHT, PAD_SIZE)
        sizer.Add(self.running_img, 0, wx.EXPAND | wx.RIGHT, PAD_SIZE)
        sizer.Add(self.check_mark, 0, wx.EXPAND | wx.RIGHT, PAD_SIZE)
        sizer.Add(self.error_symbol, 0, wx.EXPAND | wx.RIGHT, PAD_SIZE)
        self.running_img.Hide()
        self.check_mark.Hide()
        self.error_symbol.Hide()
        vsizer.Add(sizer, 1, wx.EXPAND)
        self.SetSizer(vsizer)


    def _load_image(self, imgPath, targetHeight):
        rawImage = imageutil.loadImage(imgPath)
        sizedImage = imageutil.resizeImage(rawImage, targetHeight)
        return imageutil.wrapBitmap(sizedImage, self)


    def build_heading_sizer(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.AddStretchSpacer(1)
        if self.buildSpec['header_show_title']:
            sizer.Add(self._header, 0)
        else:
            self._header.Hide()

        if self.buildSpec['header_show_subtitle']:
            sizer.Add(self._subheader, 0)
        else:
            self._subheader.Hide()
        sizer.AddStretchSpacer(1)
        return sizer

    def bindMouseEvents(self):
        """
        Manually binding all LEFT_DOWN events.
        See: gooey.gui.mouse for background.
        """
        self.Bind(wx.EVT_LEFT_DOWN, notifyMouseEvent)
        self._header.Bind(wx.EVT_LEFT_DOWN, notifyMouseEvent)
        self._subheader.Bind(wx.EVT_LEFT_DOWN, notifyMouseEvent)
        for image in self.images:
            image.Bind(wx.EVT_LEFT_DOWN, notifyMouseEvent)