import sys

from gooey.gui.processor import ProcessController
from gooey.gui.model import States
from gooey.gui.pubsub import pub
from gooey.gui import events
from gooey.gui.windows import layouts

import wx

class Presenter(object):
  def __init__(self, view, model):
    self.view = view
    self.model = model

    self.client_runner = ProcessController(
      self.model.progress_regex,
      self.model.progress_expr
    )

    pub.subscribe(self.on_cancel, events.WINDOW_CANCEL)
    pub.subscribe(self.on_stop, events.WINDOW_STOP)
    pub.subscribe(self.on_start, events.WINDOW_START)
    pub.subscribe(self.on_restart,  events.WINDOW_RESTART)
    pub.subscribe(self.on_edit, events.WINDOW_EDIT)
    pub.subscribe(self.on_close, events.WINDOW_CLOSE)

    # console statuses from the other thread
    pub.subscribe(self.on_new_message, 'console_update')
    pub.subscribe(self.on_progress_change, 'progress_update')
    pub.subscribe(self.on_client_done, 'execution_complete')


    pub.subscribe(self.on_selection_change, events.LIST_BOX)


  def on_selection_change(self, selection):
    self.update_model()
    self.model.active_group = selection
    self.redraw_from_model()
    self.syncronize_from_model()

  def initialize_view(self):
    self.view.window_title = self.model.program_name
    self.view.window_size = self.model.default_size

    self.view.required_section.clear()
    self.view.optional_section.clear()
    self.view.required_section.populate(self.model.required_args, self.model.num_required_cols)
    self.view.optional_section.populate(self.model.optional_args, self.model.num_optional_cols)

    if self.model.use_monospace_font:
      self.view.set_display_font_style('monospace')

    if self.should_disable_stop_button():
      self.view.disable_stop_button()
    else:
      self.view.enable_stop_button()

    if self.model.layout_type == layouts.COLUMN:
      self.view.set_list_contents(list(self.model.argument_groups.keys()))

    if self.model.auto_start:
      self.model.update_state(States.RUNNNING)
      self.on_start()
    self.syncronize_from_model()

  def update_model(self):
    self.update_list(self.model.required_args, self.view.required_section.get_values())
    self.update_list(self.model.optional_args, self.view.optional_section.get_values())
    self.syncronize_from_model()

  def syncronize_from_model(self):
    #TODO move this out of the presenter
    #TODO Make all view interactions thread safe
    wx.CallAfter(self.syncronize_from_model_async)

  def syncronize_from_model_async(self):
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

  def redraw_from_model(self):
    self.view.freeze()
    self.view.required_section.clear()
    self.view.optional_section.clear()
    self.view.required_section.populate(self.model.required_args, self.model.num_required_cols)
    self.view.optional_section.populate(self.model.optional_args, self.model.num_optional_cols)
    getattr(self, self.model.current_state)()
    self.view.thaw()

  def should_disable_stop_button(self):
    return self.model.stop_button_disabled

  def on_start(self):
    self.update_model()
    if not self.model.is_valid():
      return self.view.show_missing_args_dialog()
    command = self.model.build_command_line_string()
    self.client_runner.run(command)
    self.model.update_state(States.RUNNNING)
    self.syncronize_from_model()

  def on_stop(self):
    self.ask_stop()

  def on_edit(self):
    self.model.update_state(States.CONFIGURING)
    self.syncronize_from_model()

  def on_restart(self):
    self.on_start()

  def on_cancel(self):
    if self.view.confirm_exit_dialog():
      self.view.Destroy()
      sys.exit()

  def on_close(self):
    self.view.Destroy()
    sys.exit()

  def on_new_message(self, msg):
    # observes changes coming from the subprocess
    self.view.update_console_async(msg)

  def on_progress_change(self, progress):
    # observes changes coming from the subprocess
    self.view.update_progress_aync(progress, self.model.disable_progress_bar_animation)

  def on_client_done(self):
    if self.client_runner.was_success():
      self.model.update_state(States.SUCCESS)
    else:
      self.model.update_state(States.ERROR)
    self.syncronize_from_model()

  def ask_stop(self):
    if self.view.confirm_stop_dialog():
      self.stop()
      return True
    return False

  def stop(self):
    self.client_runner.stop()

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

  @staticmethod
  def partition(collection, condition):
    return filter(condition, collection), filter(lambda x: not condition(x), collection)

  def update_list(self, collection, new_values):
    # convenience method for syncronizing the model -> widget list collections
    for index, val in enumerate(new_values):
      collection[index].value = val


