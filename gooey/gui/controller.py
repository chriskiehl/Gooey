'''
Created on Dec 22, 2013

@author: Chris
'''
import subprocess
import sys
from multiprocessing.dummy import Pool, Process

import wx

from gooey.gui.lang import i18n


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

  def __init__(self, base_frame, build_spec):
    self.core_gui = base_frame
    self.build_spec = build_spec

  def OnCancelButton(self, widget, event):
    msg = i18n.translate('sure_you_want_to_exit')
    dlg = wx.MessageDialog(None, msg, i18n.translate('close_program'), wx.YES_NO)
    result = dlg.ShowModal()
    print result
    if result == YES:
      dlg.Destroy()
      self.core_gui.Destroy()
      sys.exit()
    dlg.Destroy()

  def OnStartButton(self, widget, event):
    cmd_line_args = self.core_gui.GetOptions()

    _required = self.core_gui.GetRequiredArgs()
    if _required and any(req == '' for req in _required):
      self.ShowDialog(i18n.translate('error_title'), "Must fill in all fields in the Required section!", wx.ICON_ERROR)
      return

    self.core_gui.NextPage()
    self.RunClientCode(None)

  def RunClientCode(self, process):
    def doInBackground(process, callback):
      while True:
        line = process.stdout.readline()
        if not line:
          break
        self.core_gui.PublishConsoleMsg(line)
      callback(process)

    p = subprocess.Popen(r'python C:\Users\Chris\Desktop\Untitled\prog.py', bufsize=1, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    _pool = Pool(1)
    _pool.apply_async(doInBackground, (p, self.HandleResult))

  def HandleResult(self, process):
    _stdout, _stderr = process.communicate()
    if process.returncode == 0:
      self.core_gui.NextPage()
      self.ShowGoodFinishedDialog()
    else:
      self.core_gui.NextPage()
      self.ShowBadFinishedDialog(_stderr)

  def OnRestartButton(self, widget, event):
    self.OnStartButton(self, None, event)

  def ManualStart(self):
    self.core_gui.NextPage()
    wx.CallAfter(wx.ActivateEvent)
    Process(target=self.RunClientCode).start()

  def OnCloseButton(self, widget, event):
    self.core_gui.Destroy()
    sys.exit()

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

