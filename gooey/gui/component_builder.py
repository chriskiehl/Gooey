from collections import namedtuple
from gooey.gui.widgets import components


is_required = lambda widget: widget['required']
is_checkbox = lambda widget: isinstance(widget, components.CheckBox)

ComponentList = namedtuple('ComponentList', 'required_args optional_args')

def build_components(widget_list):
  '''
  :param widget_list: list of dicts containing widget info (name, type, etc..)
  :return: ComponentList

  Converts the Json widget information into concrete wx Widget types
  '''
  required_args, optional_args  = partition(widget_list, is_required)
  checkbox_args, general_args = partition(map(build_widget, optional_args), is_checkbox)

  required_args = map(build_widget, required_args)
  optional_args = general_args + checkbox_args

  return ComponentList(required_args, optional_args)

def build_widget(widget_info):
  widget_class = getattr(components, widget_info['type'])
  return widget_class(data=widget_info['data'])

def partition(collection, condition):
  return filter(condition, collection), filter(lambda x: not condition(x), collection)

