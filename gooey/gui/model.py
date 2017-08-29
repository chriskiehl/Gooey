import os
from collections import OrderedDict, namedtuple
from itertools import chain
from gooey.gui.lang.i18n import _
from gooey.gui.util.quoting import quote

import wx

ArgumentGroup = namedtuple('ArgumentGroup', 'name command required_args optional_args')


class MyWidget(object):
  # TODO: Undumbify damn
  # TODO: Undumbify _value/value access

  def __init__(self, type, title, help, default, nargs, commands, choices):
    self.type = type
    self.title = title
    self.help = help
    self.default = default
    self._value = default
    self.nargs = nargs
    self.commands = commands
    self.choices = choices

  @property
  def value(self):
    # TODO: split into stategy or subclass thingie
    if self.type == 'CheckBox':
      return self.commands[0] if self._value else None
    if self.type == 'RadioGroup':
      try:
        return self.commands[self._value.index(True)][0]
      except ValueError:
        return None
    if self.type == 'MultiFileChooser':
      value = ' '.join(quote(x) for x in self._value.split(os.pathsep) if x)
      if self.commands and value:
        return u'{} {}'.format(self.commands[0], value)
      return value or None
    if self.type == 'Textarea':
      if self.commands and self._value:
        return '{} {}'.format(self.commands[0], quote(self._value.encode('unicode_escape')))
      else:
        return quote(self._value.encode('unicode_escape')) if self._value else ''
    if self.type == 'CommandField':
      if self.commands and self._value:
        return u'{} {}'.format(self.commands[0], self._value)
      else:
        return self._value or None

    if self.type == 'Counter':
      '''
      Returns
        str(option_string * DropDown Value)
        e.g.
        -vvvvv
      '''
      if not str(self._value).isdigit():
        return None
      arg = str(self.commands[0]).replace('-', '')
      repeated_args = arg * int(self._value)
      return '-' + repeated_args

    if self.type == 'Dropdown':
      if self._value == 'Select Option':
        return None
      elif self.commands and self._value:
        return u'{} {}'.format(self.commands[0], quote(self._value))
      else:
        return quote(self._value) if self._value else ''
    else:
      if self.commands and self._value:
        if not self.nargs:
          v = quote(self._value)
        else:
          v = self._value
        return u'{0} {1}'.format(self.commands[0], v)
      else:
        if not self._value:
          return None
        elif not self.nargs:
          return quote(self._value)
        else:
          return self._value

  @value.setter
  def value(self, val):
    self._value = val

  @classmethod
  def from_dict(cls, data):
    def maybe_unpack(collection, attr):
      # TODO: RadioGroups need to support defaults
      try:
        if isinstance(collection, list):
          return [item[attr] for item in collection]
        return collection[attr]
      except:
        return None

    details = data['data']
    return cls(
      data['type'],
      maybe_unpack(details, 'display_name'),
      maybe_unpack(details, 'help'),
      maybe_unpack(details, 'default'),
      maybe_unpack(details, 'nargs'),
      maybe_unpack(details, 'commands'),
      maybe_unpack(details, 'choices')
    )




class States(object):
  CONFIGURING = 'configuring'
  RUNNNING = 'running'
  SUCCESS = 'success'
  ERROR = 'error'
  STOPPED = 'stopped'



class MyModel(object):
  '''
  '''

  def wrap(self, groups):
    output = OrderedDict()
    for name, group in groups.items():
      output[name] = ArgumentGroup(
        name,
        group['command'],
        *self.group_arguments(group['contents'])
      )
    return output


  def __init__(self, build_spec):

    self.current_state = States.CONFIGURING

    self.build_spec = build_spec
    self.layout_type = self.build_spec.get('layout_type')

    self.auto_start = self.build_spec.get('auto_start')
    self.progress_regex = self.build_spec.get('progress_regex')
    self.progress_expr = self.build_spec.get('progress_expr')
    self.disable_progress_bar_animation = self.build_spec['disable_progress_bar_animation']

    self.program_name = self.build_spec.get('program_name')
    self.default_size = self.build_spec.get('default_size')

    self.heading_title = _("settings_title")
    self.heading_subtitle = self.build_spec['program_description'] or ''

    self.use_monospace_font = self.build_spec.get('monospace_display')
    self.stop_button_disabled = self.build_spec['disable_stop_button']

    self.argument_groups = self.wrap(self.build_spec.get('widgets', {}))
    self.active_group = next(iter(self.argument_groups))

    self.num_required_cols = self.build_spec['num_required_cols']
    self.num_optional_cols = self.build_spec['num_optional_cols']

    self.text_states = {
      States.CONFIGURING: {
        'title': _("settings_title"),
        'subtitle': self.build_spec['program_description'] or ''
      },
      States.RUNNNING: {
        'title': _("running_title"),
        'subtitle': _('running_msg')
      },
      States.SUCCESS: {
        'title': _('finished_title'),
        'subtitle': _('finished_msg')
      },
      States.ERROR: {
        'title': _('finished_title'),
        'subtitle': _('finished_error')
      }
    }

  @property
  def required_args(self):
    return self.argument_groups[self.active_group].required_args

  @property
  def optional_args(self):
    return self.argument_groups[self.active_group].optional_args

  def update_state(self, state):
    self.current_state = state

    text = self.text_states[state]
    self.heading_title = text['title']
    self.heading_subtitle = text['subtitle']

  def is_valid(self):
    # TODO: fix skipping_config.. whatever that did
    # currently breaks when you supply it as a decorator option
    # return self.skipping_config() and self.required_section_complete()
    return self.is_required_section_complete()

  def skipping_config(self):
    return self.build_spec['manual_start']

  def is_required_section_complete(self):
    error_found = False
    for arg in self.required_args:
      widget = arg.widget_instance.widget_pack.widget
      if arg.value:
        widget.SetBackgroundColour(wx.NullColour)
      else:
        if not error_found:
          error_found = True
          widget.SetFocus()
        widget.SetBackgroundColour("#EF9A9A")

      widget.Refresh()

    return not error_found

  def build_command_line_string(self):
    optional_args = [arg.value for arg in self.optional_args]
    required_args = [c.value for c in self.required_args if c.commands]
    position_args = [c.value for c in self.required_args if not c.commands]
    if position_args:
      position_args.insert(0, "--")
    cmd_string = ' '.join(list(filter(None, chain(required_args, optional_args, position_args))))
    if self.layout_type == 'column':
      cmd_string = u'{} {}'.format(self.argument_groups[self.active_group].command, cmd_string)
    return u'{} --ignore-gooey {}'.format(self.build_spec['target'], cmd_string)

  def group_arguments(self, widget_list):
    is_required = lambda widget: widget['required']
    not_checkbox = lambda widget: widget['type'] != 'CheckBox'

    required_args, optional_args  = self.partition(widget_list, is_required)
    if self.build_spec['group_by_type']:
      optional_args = chain(*self.partition(optional_args, not_checkbox))
    return list(map(self.to_object, required_args)), list(map(self.to_object, optional_args))

  @staticmethod
  def partition(collection, condition):
    return list(filter(condition, collection)), list(filter(lambda x: not condition(x), collection))

  def to_object(self, data):
    details = data['data']
    return MyWidget(
      data['type'],
      self.maybe_unpack(details, 'display_name'),
      self.maybe_unpack(details, 'help'),
      self.maybe_unpack(details, 'default'),
      self.maybe_unpack(details, 'nargs'),
      self.maybe_unpack(details, 'commands'),
      self.maybe_unpack(details, 'choices')
    )

  @staticmethod
  def maybe_unpack(collection, attr):
    # TODO: RadioGroups need to support defaults
    try:
      if isinstance(collection, list):
        return [item[attr] for item in collection]
      return collection[attr]
    except:
      return None



