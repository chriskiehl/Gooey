'''
Created on Dec 23, 2013

@author: Chris
'''

import wx
import wx.animate
from gooey import i18n
from gooey.gui import imageutil
from gooey import image_repository


class AbstractFooter(wx.Panel):
  '''
  Abstract class for the Footer panels.
  '''

  def __init__(self, parent, **kwargs):
    wx.Panel.__init__(self, parent, **kwargs)
    self.SetMinSize((30, 53))

    self._controller = None

    # components
    self.cancel_button = None
    self.start_button = None
    self.running_animation = None
    self.close_button = None

    self._init_components()
    self._init_pages()
    self._do_layout()


  def _init_components(self):
    '''
    initialize all of the gui used in the footer
    TODO:
      Add Checkmark image for when the program has finished running.
      Refactor image tools into their own module. The resize code is
      getting spread around a bit.
    '''
    self.cancel_button = self._Button(i18n.translate('cancel'), wx.ID_CANCEL)
    self.start_button = self._Button(i18n.translate('start'), wx.ID_OK)
    self.running_animation = wx.animate.GIFAnimationCtrl(self, -1, image_repository.loader)
    self.close_button = self._Button(i18n.translate("close"), wx.ID_OK)

  def _init_pages(self):

    def PageOne():
      self.cancel_button.Hide()
      self.start_button.Hide()
      self.running_animation.Show()
      self.running_animation.Play()
      self.Layout()

    def PageTwo():
      self.running_animation.Stop()
      self.running_animation.Hide()
      self.close_button.Show()
      self.Layout()

    self._pages = iter([PageOne, PageTwo])


  def _do_layout(self):
    v_sizer = wx.BoxSizer(wx.VERTICAL)
    h_sizer = wx.BoxSizer(wx.HORIZONTAL)

    h_sizer.AddStretchSpacer(1)
    h_sizer.Add(self.cancel_button, 0, wx.ALIGN_RIGHT | wx.RIGHT, 20)
    h_sizer.Add(self.start_button, 0, wx.ALIGN_RIGHT | wx.RIGHT, 20)

    v_sizer.AddStretchSpacer(1)
    v_sizer.Add(h_sizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND)
    v_sizer.Add(self.running_animation, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.RIGHT, 20)
    self.running_animation.Hide()
    v_sizer.Add(self.close_button, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.RIGHT, 20)
    self.close_button.Hide()
    v_sizer.AddStretchSpacer(1)
    self.SetSizer(v_sizer)

  def _Button(self, label=None, style=None):
    return wx.Button(
      parent=self,
      id=-1,
      size=(90, 24),
      label=label,
      style=style)

  def RegisterController(self, controller):
    if self._controller is None:
      self._controller = controller

  def NextPage(self):
    next(self._pages)()

  def _load_image(self, img_path, height=70):
    return imageutil.resize_bitmap(
      self,
      imageutil._load_image(img_path),
      height)


class Footer(AbstractFooter):
  '''
  Footer section used on the configuration
  screen of the application

  args:
    parent: wxPython parent window
    controller: controller class used in delagating all the commands
  '''

  def __init__(self, parent, controller, **kwargs):
    AbstractFooter.__init__(self, parent, **kwargs)

    self.Bind(wx.EVT_BUTTON, self.OnCancelButton, self.cancel_button)
    self.Bind(wx.EVT_BUTTON, self.OnStartButton, self.start_button)
    self.Bind(wx.EVT_BUTTON, self.OnCloseButton, self.close_button)

  def OnCancelButton(self, event):
    self._controller.OnCancelButton(self, event)
    event.Skip()

  def OnCloseButton(self, event):
    self._controller.OnCloseButton(self, event)
    event.Skip()

  def OnStartButton(self, event):
    self._controller.OnStartButton(event, self)
    event.Skip()

