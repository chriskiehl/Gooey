'''
Created on Dec 22, 2013

@author: Chris
'''

import wx
import sys
import traceback

from gooey import i18n
from multiprocessing.dummy import Pool, Process

YES = 5103
NO = 5104


class Controller(object):
  '''
  Main controller for the gui.

  All controlls are delegated to this central control point.

  Args:
    base_frame	 = Reference to the Basewindow
    head_panel	 = reference to the BaseWindow's Head Panel
    body_panel 	 = reference to the BaseWindow's Body Panel
    footer_panel = reference to the BaseWindow's Footer Panel
    model				 = configuration model
    translator	 = instance of the I18N class
  '''

  def __init__(
      self, base_frame, head_panel, body_panel,
      footer_panel, model):
    self._base = base_frame
    self._head = head_panel
    self._body = body_panel
    self._foot = footer_panel

    self._model = model
    self._payload_runner = Process(target=self.RunClientCode)

  def OnCancelButton(self, widget, event):
    msg = i18n.translate('sure_you_want_to_exit')
    dlg = wx.MessageDialog(None, msg,
                           i18n.translate('close_program'), wx.YES_NO)
    result = dlg.ShowModal()
    print result
    if result == YES:
      dlg.Destroy()
      self._base.Destroy()
      sys.exit()
    dlg.Destroy()

  def OnStartButton(self, widget, event):
    cmd_line_args = self._body.GetOptions()
    if not self._model.IsValidArgString(cmd_line_args):
      error_msg = self._model.GetErrorMsg(cmd_line_args)
      self.ShowDialog(i18n.translate('error_title'), error_msg, wx.ICON_ERROR)
      return
    self._model.AddToArgv(cmd_line_args)
    self._base.NextPage()
    self._payload_runner.start()

  def ManualStart(self):
    self._base.NextPage()
    wx.CallAfter(wx.ActivateEvent)
    self._payload_runner.start()

  def OnCloseButton(self, widget, event):
    self._base.Destroy()
    sys.exit()

  def RunClientCode(self):
    pool = Pool(1)
    try:
      pool.apply(self._base._payload)
      self._head.NextPage()
      self._foot.NextPage()
      self.ShowGoodFinishedDialog()
    except:
      self.ShowBadFinishedDialog(traceback.format_exc())

  def ShowGoodFinishedDialog(self):
    self.ShowDialog(i18n.translate("execution_finished"),
                    i18n.translate('success_message'),
                    wx.ICON_INFORMATION)

  def ShowBadFinishedDialog(self, error_msg):
    msg = i18n.translate('uh_oh').format(error_msg)
    self.ShowDialog(i18n.translate('error_title'), msg, wx.ICON_ERROR)


  def ShowDialog(self, title, content, style):
    a = wx.MessageDialog(None, content, title, style)
    a.ShowModal()
    a.Destroy()

