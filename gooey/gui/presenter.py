from collections import namedtuple

from gooey.gui import component_builder
from gooey.gui.lang.i18n import _
from gooey.gui.pubsub import pub
from gooey.gui import events

class Presenter(object):
  def __init__(self, view, model):
    self.view = view
    self.model = model

    pub.subscribe(self.on_start,    events.WINDOW_START)

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
    cmd_line_args = self.model.build_command_line_string()
    print cmd_line_args

    # cmd_line_args = self.view.GetOptions()
    # command = '{} --ignore-gooey {}'.format(self.build_spec['target'], cmd_line_args)
    # pub.send_message(events.WINDOW_CHANGE, view_name=views.RUNNING_SCREEN)
    # self.run_client_code(command)

  def update_model(self):
    self.update_list(self.model.required_args, self.view.required_section.get_values())
    self.update_list(self.model.optional_args, self.view.optional_section.get_values())


  def update_list(self, collection, new_values):
    for index, val in enumerate(new_values):
      collection[index].value = val


  @staticmethod
  def partition(collection, condition):
    return filter(condition, collection), filter(lambda x: not condition(x), collection)

  def syncronize_from_model(self):
    self.view.heading_title = self.model.heading_title
    self.view.heading_subtitle = self.model.heading_subtitle

  def should_disable_stop_button(self):
    return self.model.stop_button_disabled



