import itertools

from gooey.gui.widgets import components2


class ComponentBuilder(object):
  def __init__(self, build_spec):
    self.build_spec = build_spec
    _required_specs = self.build_spec.get('required', None)
    _optional_specs = self.build_spec.get('optional', None)

    self.required_args = self.build_widget(_required_specs) if _required_specs else None

    optionals = self.build_widget(_optional_specs) if _optional_specs else None
    if _optional_specs:
      self.flags = [widget for widget in optionals if isinstance(widget, components2.CheckBox)]
      self.general_options = [widget for widget in optionals if not isinstance(widget, components2.CheckBox)]
    else:
      self.flags = []
      self.general_options = []

  def build_widget(self, build_spec):
    assembled_widgets = []
    for spec in build_spec:
      widget_type = spec['type']
      properties = spec['data']

      Component = getattr(components2, widget_type)
      assembled_widgets.append(Component(data=properties))
    return assembled_widgets


  def __iter__(self):
    '''
    return an iterator for all of the contained gui
    '''
    return itertools.chain(self.required_args or [],
                           self.flags or [],
                           self.general_options or [])

