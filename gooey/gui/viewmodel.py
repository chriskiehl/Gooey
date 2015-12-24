from itertools import chain

from gooey.gui.widgets import components


is_required = lambda widget: widget['required']
is_checkbox = lambda widget: widget['type'] == 'CheckBox'

class ViewModel(object):

  def __init__(self, build_spec):
    self.config = build_spec
    self.fields = []
    self.required_fields = []
    self.optional_fields = []

    required_args, optional_args  = partition(build_spec['widgets'], is_required)
    checkbox_args, general_args = partition(optional_args, is_checkbox)

    self.required_fields = map(self.field_dispatch, required_args)
    self.optional_fields = map(self.field_dispatch, general_args + checkbox_args)

    print self.required_fields
    print self.optional_fields

  def field_dispatch(self, data):
    if data['type'] == 'RadioGroup':
      return MultiField(data)
    return Field(data)

  def required_section_complete(self):
    required_args_present = map(lambda x: x.value, self.fields)

    return bool(required_args_present and all(required_args_present))

  def skipping_config(self):
    return self.config['manual_start']

  def build_cmd_string(self):
    _f = lambda lst: [x for x in lst if x is not None]
    optional_args = _f([c.GetValue() for c in self.optional_fields])
    required_args = _f([c.GetValue() for c in self.required_fields if c.HasOptionString()])
    position_args = _f([c.GetValue() for c in self.required_fields if not c.HasOptionString()])
    if position_args: position_args.insert(0, "--")
    return ' '.join(chain(required_args, optional_args, position_args))

  def validate(self):
    errors = []
    for field in self.fields:
      if not field.is_valid():
        errors.append({field.name: field.errors})



class MultiField(object):

  def __init__(self, widget):
    self.required = widget['required']
    self.wxwidget = self._prime(widget)
    self.type = widget['type']

    self.nargs = self._unwrap_fields('nargs', widget['data'])
    self.command = self._unwrap_cmds(widget['data'])
    self.display_name = self._unwrap_fields('display_name', widget['data'])
    self.help = self._unwrap_fields('help', widget['data'])
    self.choices = self._unwrap_fields('choices', widget['data'])

  def _prime(self, widget):
    # pre-builds the widget
    widget_class = getattr(components, widget['type'])
    return widget_class(data=widget['data'])


  def _unwrap_fields(self, key, collection):
    return [data[key] for data in collection]

  def _unwrap_cmds(self, collection):
    return [x['commands'][0] if x['commands'] else ''
            for x in collection]

  def build(self, parent):
    return self.wxwidget.build(parent)

class Field(object):

  def __init__(self, widget):
    data = widget['data']

    self.required = widget['required']
    self.wxwidget = self._prime(widget)
    self.type = widget['type']

    self.nargs = data['nargs']
    self.command = data['commands'][0] if data['commands'] else ''
    self.display_name = data['display_name']
    self.help = data['help']
    self.choices = data['choices']

  def __str__(self):
    return '{0}: {1}'.format(self.display_name, self.type)

  def _prime(self, widget):
    # pre-builds the widget
    widget_class = getattr(components, widget['type'])
    return widget_class(data=widget['data'])

  @property
  def value(self):
    return self.wxwidget.GetValue()

  @value.setter
  def value(self, val):
    self.wxwidget.setValue(val)

  def validate(self):
    pass

  def build(self, parent):
    return self.wxwidget.build(parent)


def build_widget(widget_info):
  widget_class = getattr(components, widget_info['type'])
  return widget_class(data=widget_info['data'])

def partition(collection, condition):
  return filter(condition, collection), filter(lambda x: not condition(x), collection)

