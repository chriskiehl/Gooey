'''
Created on Dec 22, 2013

@author: Chris
'''

import wx
import sys
import subprocess

from gooey.gui.pubsub import pub

from multiprocessing.dummy import Pool
from gooey.gui import events
from gooey.gui.lang import i18n
from gooey.gui.windows import views

YES = 5103
NO = 5104



class Controller(object):
  '''
  Main controller for the gui.

  All controlls are delegated to this central control point.
  '''

  def __init__(self, base_frame, build_spec):
    '''
    :type base_frame: BaseWindow
    :type build_spec: dict
    '''
    self.core_gui = base_frame
    self.build_spec = build_spec

    # wire up all the observers
    pub.subscribe(self.on_cancel,   events.WINDOW_CANCEL)
    pub.subscribe(self.on_start,    events.WINDOW_START)
    pub.subscribe(self.on_restart,  events.WINDOW_RESTART)
    pub.subscribe(self.on_close,    events.WINDOW_CLOSE)
    pub.subscribe(self.on_edit,     events.WINDOW_EDIT)

  def on_edit(self):
    pub.send_message(events.WINDOW_CHANGE, view_name=views.CONFIG_SCREEN)

  def on_close(self):
    self.core_gui.Destroy()
    sys.exit()

  def on_restart(self):
    self.on_start()

  def manual_restart(self):
    self.on_start()

  def on_cancel(self):
    msg = i18n._('sure_you_want_to_exit')
    dlg = wx.MessageDialog(None, msg, i18n._('close_program'), wx.YES_NO)
    result = dlg.ShowModal()
    if result == YES:
      dlg.Destroy()
      self.core_gui.Destroy()
      sys.exit()
    dlg.Destroy()

  def on_start(self):
    if not self.skipping_config() and not self.required_section_complete():
      return self.show_dialog(i18n._('error_title'), i18n._('error_required_fields'), wx.ICON_ERROR)

    cmd_line_args = self.core_gui.GetOptions()
    command = '{0} --ignore-gooey {1}'.format(self.build_spec['target'], cmd_line_args)
    pub.send_message(events.WINDOW_CHANGE, view_name=views.RUNNING_SCREEN)
    self.run_client_code(command)

  def run_client_code(self, command):
    p = subprocess.Popen(command, bufsize=1, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    pool = Pool(1)
    pool.apply_async(self.read_stdout, (p, self.process_result))

  def read_stdout(self, process, callback):
    while True:
      line = process.stdout.readline()
      if not line:
        break
      wx.CallAfter(self.core_gui.PublishConsoleMsg, line)
    wx.CallAfter(callback, process)

  def process_result(self, process):
    _stdout, _stderr = process.communicate()
    if process.returncode == 0:
      pub.send_message(events.WINDOW_CHANGE, view_name=views.SUCCESS_SCREEN)
      self.success_dialog()
    else:
      pub.send_message(events.WINDOW_CHANGE, view_name=views.ERROR_SCREEN)
      self.error_dialog(_stderr)

  def skipping_config(self):
    return self.build_spec['manual_start']

  def required_section_complete(self):
    required_section = self.core_gui.GetRequiredArgs()
    if len(required_section) == 0:
      return True  # no requirements!
    return not any(req == '' for req in required_section)

  def success_dialog(self):
    self.show_dialog(i18n._("execution_finished"), i18n._('success_message'), wx.ICON_INFORMATION)

  def error_dialog(self, error_msg):
    self.show_dialog(i18n._('error_title'), i18n._('uh_oh').format(error_msg), wx.ICON_ERROR)

  def show_dialog(self, title, content, style):
    a = wx.MessageDialog(None, content, title, style)
    a.ShowModal()
    a.Destroy()

