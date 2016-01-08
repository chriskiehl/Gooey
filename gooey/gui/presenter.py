import re
from collections import namedtuple

import subprocess

from gooey.gui import component_builder
from gooey.gui.controller2 import ProcessController
from gooey.gui.lang.i18n import _
from gooey.gui.model import States
from gooey.gui.pubsub import pub
from gooey.gui import events
from gooey.gui.windows import views
from multiprocessing.dummy import Pool

class Presenter(object):
  def __init__(self, view, model):
    self.view = view
    self.model = model
    self.client_runner = ProcessController(
      self.model.progress_regex,
      self.model.progress_expr
    )

    pub.subscribe(self.on_start, events.WINDOW_START)

    # console statuses from the other thread
    pub.subscribe(self.on_new_message, 'console_update')
    pub.subscribe(self.on_progress_change, 'progress_update')
    pub.subscribe(self.on_client_done, 'execution_complete')


  def initialize_view(self):
    self.view.window_title = self.model.program_name
    self.view.window_size = self.model.default_size

    self.view.required_section.populate(self.model.required_args)
    self.view.optional_section.populate(self.model.optional_args)

    if self.model.use_monospace_font:
      self.view.set_display_font_style('monospace')

    if self.should_disable_stop_button():
      self.view.disable_stop_button()
    else:
      self.view.enable_stop_button()

    self.syncronize_from_model()


  def on_start(self):
    self.update_model()
    if not self.model.is_valid():
      self.view.show_missing_args_dialog()
    command = self.model.build_command_line_string()
    self.client_runner.run(command)

    self.model.update_state(States.RUNNNING)
    self.syncronize_from_model()

  def on_new_message(self, msg):
    # observes changes coming from the subprocess
    self.view.update_console_async(msg)

  def on_progress_change(self, progress):
    # observes changes coming from the subprocess
    print 'Progress:', progress
    self.view.update_progress_aync(progress)

  def on_client_done(self):
    if self.client_runner.was_success():
      self.model.update_state(States.SUCCESS)
    else:
      self.model.update_state(States.ERROR)
    self.syncronize_from_model()




  def update_model(self):
    self.update_list(self.model.required_args, self.view.required_section.get_values())
    self.update_list(self.model.optional_args, self.view.optional_section.get_values())
    self.syncronize_from_model()


  def update_list(self, collection, new_values):
    for index, val in enumerate(new_values):
      collection[index].value = val

  @staticmethod
  def partition(collection, condition):
    return filter(condition, collection), filter(lambda x: not condition(x), collection)

  def syncronize_from_model(self):
    # update heading titles
    self.view.heading_title = self.model.heading_title
    self.view.heading_subtitle = self.model.heading_subtitle

    # refresh the widgets
    for index, widget in enumerate(self.view.required_section):
      widget.set_value(self.model.required_args[index]._value)
    for index, widget in enumerate(self.view.optional_section):
      widget.set_value(self.model.optional_args[index]._value)

    # swap the views
    getattr(self, self.model.current_state)()

  def should_disable_stop_button(self):
    return self.model.stop_button_disabled

  def configuring(self):
    self.view.hide_all_buttons()
    self.view.hide('check_mark', 'running_img', 'error_symbol', 'runtime_display')
    self.view.show('settings_img', 'cancel_button', 'start_button', 'config_panel')
    self.view.Layout()

  def running(self):
    self.view.hide_all_buttons()
    self.view.hide('check_mark', 'settings_img', 'error_symbol', 'config_panel')
    self.view.show('running_img', 'stop_button', 'progress_bar', 'runtime_display')
    self.view.progress_bar.Pulse()
    self.view.Layout()

  def success(self):
    self.view.hide_all_buttons()
    self.view.hide('running_img', 'progress_bar', 'config_panel')
    self.view.show('check_mark', 'edit_button', 'restart_button', 'close_button', 'runtime_display')
    self.view.Layout()

  def error(self):
    self.view.hide_all_buttons()
    self.view.hide('running_img', 'progress_bar', 'config_panel')
    self.view.show('error_symbol', 'edit_button', 'restart_button', 'close_button', 'runtime_display')
    self.view.Layout()

  # def process_result(self, process):
  #   _stdout, _ = process.communicate()
  #   if process.returncode == 0:
  #     self.model.update_state(States.SUCCESS)
  #     self.syncronize_from_model()
  #     # pub.send_message(events.WINDOW_CHANGE, view_name=views.SUCCESS_SCREEN)
  #     # self.success_dialog()
  #   else:
  #     self.model.update_state(States.ERROR)
  #     self.syncronize_from_model()
  #     # pub.send_message(events.WINDOW_CHANGE, view_name=views.ERROR_SCREEN)
  #     # self.error_dialog()

  # # FOOTER
  # def _init_pages(self):
  #   def config():
  #     self.hide_all_buttons()
  #     self.cancel_button.Show()
  #     self.start_button.Show()
  #     self.Layout()
  #
  #   def running():
  #     self.hide_all_buttons()
  #     self.stop_button.Show()
  #     self.progress_bar.Show()
  #     self.progress_bar.Pulse()
  #     self.Layout()
  #
  #   def success():
  #     self.hide_all_buttons()
  #     self.progress_bar.Hide()
  #     self.edit_button.Show()
  #     self.restart_button.Show()
  #     self.close_button.Show()
  #     self.Layout()
  #
  #   def error():
  #     success()
  #
  #   self.layouts = locals()
  #
  # # BODY
  # def _init_pages(self):
  #
  #   def config():
  #     self.config_panel.Show()
  #     self.runtime_display.Hide()
  #
  #   def running():
  #     self.config_panel.Hide()
  #     self.runtime_display.Show()
  #     self.Layout()
  #
  #   def success():
  #     running()
  #
  #   def error():
  #     running()
  #
  #   self.layouts = locals()
