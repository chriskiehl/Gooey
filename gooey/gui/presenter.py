from collections import namedtuple

from gooey.gui import component_builder
from gooey.gui.lang.i18n import _

is_required = lambda widget: widget['required']

SimpleArg = namedtuple('SimpleArg', 'title msg type')



class Presenter(object):
  def __init__(self, view, build_spec):
    self.view = view
    self.build_spec = build_spec

  def initialize_view(self):
    self.view.window_title = self.build_spec['program_name']
    self.view.window_size = self.build_spec['default_size']

    # widgets = component_builder.build_components(self.build_spec['widgets'])
    required_args, optional_args  = self.partition(self.build_spec['widgets'], is_required)
    self.view.required_section.populate([SimpleArg(x['data']['display_name'], x['data']['help'], x['type']) for x in required_args])


    optionals = []
    for x in optional_args:
      if x['type'] != 'RadioGroup':
        optionals.append(SimpleArg(x['data']['display_name'], x['data']['help'], x['type']))
      else:
        names = [y['display_name'] for y in x['data']]
        msgs = [y['help'] for y in x['data']]
        optionals.append(SimpleArg(names, msgs, x['type']))

    self.view.optional_section.populate(optionals)

    # self.view.optional_section.populate(widgets.optional_args)

    if self.build_spec.get('monospace_display'):
      self.view.set_display_font_style('monospace')

    if self.should_disable_stop_button():
      self.view.disable_stop_button()
    else:
      self.view.enable_stop_button()

    self.syncronize_from_model()

  @staticmethod
  def partition(collection, condition):
    return filter(condition, collection), filter(lambda x: not condition(x), collection)

  def syncronize_from_model(self):
    self.view.heading_title = _("settings_title")
    self.view.heading_subtitle = self.build_spec['program_description'] or ''

  #
  # def _init_pages(self):
  #   def config():
  #     self.view.heading_title = 'asdf'
  #     self.view.heading_subtitle = 'asdf'
  #     self.view.show('settings_img')
  #     self.view.hide('check_mark', 'running_img', 'error_symbol')
  #
  #   def running():
  #     self.view._header.SetLabel(_("running_title"))
  #     self.view._subheader.SetLabel(_('running_msg'))
  #     self.view._check_mark.Hide()
  #     self.view._settings_img.Hide()
  #     self.view._running_img.Show()
  #     self.view._error_symbol.Hide()
  #     self.view.Layout()
  #
  #   def success():
  #     self.view._header.SetLabel(_('finished_title'))
  #     self.view._subheader.SetLabel(_('finished_msg'))
  #     self.view._running_img.Hide()
  #     self.view._check_mark.Show()
  #     self.view.Layout()
  #
  #   def error():
  #     self.view._header.SetLabel(_('finished_title'))
  #     self.view._subheader.SetLabel(_('finished_error'))
  #     self.view._running_img.Hide()
  #     self.view._error_symbol.Show()
  #     self.view.Layout()
  #
  #   self.layouts = locals()



  def is_column_layout(self):
    return self.build_spec['layout_type'] == 'column'

  def should_disable_stop_button(self):
    return self.build_spec['disable_stop_button']



