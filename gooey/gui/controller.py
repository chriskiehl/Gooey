import os
import re
import wx
import sys

import subprocess

from multiprocessing.dummy import Pool

from gooey.gui.lang import i18n
from gooey.gui import events
from gooey.gui.model import MyModel
from gooey.gui.presenter import Presenter
from gooey.gui.pubsub import pub
from gooey.gui.util.taskkill import taskkill
from gooey.gui.viewmodel import ViewModel
from gooey.gui.windows import views
from gooey.gui.windows.base_window import BaseWindow


YES = 5103
NO = 5104

class Controller(object):

  def __init__(self, build_spec):
    # todo: model!
    self.build_spec = build_spec
    self.view = BaseWindow(build_spec, layout_type=self.build_spec['layout_type'])
    self.presentation = Presenter(self.view, MyModel(self.build_spec))
    self.presentation.initialize_view()

    self._process = None

    # wire up all the observers
    pub.subscribe(self.on_cancel,   events.WINDOW_CANCEL)
    pub.subscribe(self.on_stop,     events.WINDOW_STOP)
    # pub.subscribe(self.on_start,    events.WINDOW_START)
    pub.subscribe(self.on_restart,  events.WINDOW_RESTART)
    pub.subscribe(self.on_close,    events.WINDOW_CLOSE)
    pub.subscribe(self.on_edit,     events.WINDOW_EDIT)

  def on_edit(self):
    pub.send_message(events.WINDOW_CHANGE, view_name=views.CONFIG_SCREEN)

  def on_close(self):
    if self.ask_stop():
      self.view.Destroy()
      sys.exit()

  def on_restart(self):
    self.on_start()

  def manual_restart(self):
    self.on_start()

  def on_cancel(self):
    msg = i18n._('sure_you_want_to_exit')
    result = self.view.show_dialog(msg, i18n._('close_program'), wx.YES_NO)
    if result == YES:
      self.view.Destroy()
      sys.exit()

  def on_start(self):
    print self.presentation.view.required_section.get_values()
    print self.presentation.view.optional_section.get_values()
    # if not self.skipping_config() and not self.required_section_complete():
    #   return self.view.show_dialog(i18n._('error_title'), i18n._('error_required_fields'), wx.ICON_ERROR)
    #
    # cmd_line_args = self.view.GetOptions()
    # command = '{} --ignore-gooey {}'.format(self.build_spec['target'], cmd_line_args)
    # pub.send_message(events.WINDOW_CHANGE, view_name=views.RUNNING_SCREEN)
    # self.run_client_code(command)

  def on_stop(self):
    self.ask_stop()

  def ask_stop(self):
    if not self.running():
      return True
    if self.build_spec['disable_stop_button']:
      return False
    msg = i18n._('sure_you_want_to_stop')
    result = self.view.show_dialog(msg, i18n._('stop_task'), wx.YES_NO)
    if result == YES:
      self.stop()
      return True
    return False

  def stop(self):
    if self.running():
      taskkill(self._process.pid)

  def running(self):
    return self._process and self._process.poll() is None

  def run_client_code(self, command):
    env = os.environ.copy()
    env["GOOEY"] = "1"
    print "run command:", command
    p = subprocess.Popen(command, bufsize=1, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT, shell=True, env=env)
    self._process = p
    pool = Pool(1)
    pool.apply_async(self.read_stdout, (p, self.process_result))

  def read_stdout(self, process, callback):
    while True:
      line = process.stdout.readline()
      if not line:
        break
      wx.CallAfter(self.view.PublishConsoleMsg, line)
      progress = self.progress_from_line(line)
      if progress is not None:
        wx.CallAfter(self.view.UpdateProgressBar, progress)
    wx.CallAfter(callback, process)

  def progress_from_line(self, text):
    progress_regex = self.build_spec['progress_regex']
    if not progress_regex:
      return None
    match = re.search(progress_regex, text.strip())
    if not match:
      return None
    progress_expr = self.build_spec['progress_expr']
    if progress_expr:
      return self._eval_progress(match, progress_expr)
    else:
      return self._search_progress(match)

  def _search_progress(self, match):
    try:
      return int(float(match.group(1)))
    except:
      return None

  def _eval_progress(self, match, eval_expr):
    def safe_float(x):
      try:
        return float(x)
      except ValueError:
        return x
    _locals = {k: safe_float(v) for k, v in match.groupdict().items()}
    if "x" not in _locals:
      _locals["x"] = [safe_float(x) for x in match.groups()]
    try:
      return int(float(eval(eval_expr, {}, _locals)))
    except:
      return None

  def process_result(self, process):
    _stdout, _ = process.communicate()
    if process.returncode == 0:
      pub.send_message(events.WINDOW_CHANGE, view_name=views.SUCCESS_SCREEN)
      self.success_dialog()
    else:
      pub.send_message(events.WINDOW_CHANGE, view_name=views.ERROR_SCREEN)
      self.error_dialog()

  # def skipping_config(self):
  #   return self.build_spec['manual_start']
  #
  # def required_section_complete(self):
  #   required_section = self.view.GetRequiredArgs()
  #   if len(required_section) == 0:
  #     return True  # no requirements!
  #   return not any(req == '' for req in required_section)

  def success_dialog(self):
    self.view.show_dialog(i18n._("execution_finished"), i18n._('success_message'), wx.ICON_INFORMATION)

  def error_dialog(self):
    self.view.show_dialog(i18n._('error_title'), i18n._('uh_oh'), wx.ICON_ERROR)

  def run(self):
    self.view.Show(True)

