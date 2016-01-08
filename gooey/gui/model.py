import os
from itertools import chain
from gooey.gui.lang.i18n import _
from gooey.gui.util.quoting import quote


class MyWidget(object):
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
        return '{} {}'.format(self.commands[0], value)
      return value or None
    # if self.type == 'TextField':
    #   if self.commands and self._value:
    #     return '{} {}'.format(self.commands[0], quote(self._value))
    #   else:
    #     return quote(self._value) if self._value else ''
    if self.type == 'CommandField':
      if self.commands and self._value:
        return '{} {}'.format(self.commands[0], self._value)
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
      if self._value == self.default:
        return ''
      elif self.commands and self._value:
        return '{} {}'.format(self.commands[0], quote(self._value))
      else:
        return quote(self._value) if self._value else ''
    else:
      if self.commands and self._value:
        return '{0} {1}'.format(self.commands[0], quote(self._value))
      else:
        return quote(self._value) if self._value else None

  @value.setter
  def value(self, val):
    self._value = val



class States(object):
  CONFIGURING = 'configuring'
  RUNNNING = 'running'
  SUCCESS = 'success'
  ERROR = 'error'
  STOPPED = 'stopped'


class MyModel(object):
  '''
  Needs to:
  - sort the args based on a strategy
  -
  '''

  def __init__(self, build_spec):

    self.current_state = States.CONFIGURING

    self.build_spec = build_spec
    self.progress_regex = self.build_spec['progress_regex']
    self.progress_expr = self.build_spec['progress_expr']
    self.program_name = self.build_spec['program_name']
    self.default_size = self.build_spec['default_size']

    self.heading_title = _("settings_title")
    self.heading_subtitle = self.build_spec['program_description'] or ''

    self.use_monospace_font = self.build_spec.get('monospace_display')
    self.stop_button_disabled = self.build_spec['disable_stop_button']

    reqs, opts = self.group_arguments(self.build_spec['widgets'])
    self.required_args = reqs
    self.optional_args = opts

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
    completed_values = filter(None, [arg.value for arg in self.required_args])
    return len(self.required_args) == len(completed_values)

  def build_command_line_string(self):
    optional_args = [arg.value for arg in self.optional_args]
    required_args = [c.value for c in self.required_args if c.commands]
    position_args = [c.value for c in self.required_args if not c.commands]
    if position_args:
      position_args.insert(0, "--")
    cmd_string = ' '.join(filter(None, chain(required_args, optional_args, position_args)))
    return '{} --ignore-gooey {}'.format(self.build_spec['target'], cmd_string)

  def group_arguments(self, widget_list):
    is_required = lambda widget: widget['required']
    not_checkbox = lambda widget: widget['type'] != 'CheckBox'

    required_args, optional_args  = self.partition(widget_list, is_required)
    if self.build_spec['group_by_type']:
      optional_args = chain(*self.partition(optional_args, not_checkbox))
    return map(self.to_object, required_args), map(self.to_object, optional_args)

  @staticmethod
  def partition(collection, condition):
    return filter(condition, collection), filter(lambda x: not condition(x), collection)

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



