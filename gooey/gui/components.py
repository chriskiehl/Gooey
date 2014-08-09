'''
Created on Jan 1, 2014

@author: Chris

TODO: 
  Sanitize all GetValue inputs
  (to check that there's actual data there.
'''

import wx
from abc import ABCMeta
from abc import abstractmethod
from gooey.gui import styling

EMPTY = ''


class BuildException(RuntimeError):
  pass


class AbstractComponent(object):
  '''
  Template pattern-y abstract class for the gui.
  Children must all implement the BuildWidget and getValue
  methods.
  '''
  __metaclass__ = ABCMeta

  def __init__(self):
    self._widget = None
    self.msg = EMPTY

  def Build(self, parent):
    self._widget = self.BuildInputWidget(parent, self._action)
    if self.HasHelpMsg(self._action):
      self._msg = self.CreateHelpMsgWidget(parent, self._action)
    else:
      self._msg = None

    sizer = wx.BoxSizer(wx.VERTICAL)
    sizer.Add(self.CreateNameLabelWidget(parent, self._action))
    sizer.AddSpacer(2)

    if self._msg:
      sizer.Add(self._msg, 0, wx.EXPAND)
      sizer.AddSpacer(2)
    else:
      sizer.AddStretchSpacer(1)

    sizer.AddStretchSpacer(1)
    sizer.Add(self._widget, 0, wx.EXPAND)
    return sizer

  @abstractmethod
  def BuildInputWidget(self, parent, action):
    ''' Must construct the main widget type for the Action '''
    pass

  def HasHelpMsg(self, action):
    return action.help is not None

  def CreateHelpMsgWidget(self, parent, action):
    base_text = wx.StaticText(parent, label=action.help)
    if self.HasNargs(action):
      base_text += self.CreateNargsMsg(action)
    styling.MakeDarkGrey(base_text)
    return base_text

  def HasNargs(self, action):
    return action.nargs == '+' or action.nargs == '?'

  def CreateNargsMsg(self, action):
    return ' (Note: at least 1 or more arguments are required'

  def CreateNameLabelWidget(self, parent, action):
    label = str(action.dest).title()
    if len(action.option_strings) > 1:
      label += ' (%s)' % action.option_strings[0]
    text = wx.StaticText(parent, label=label)
    styling.MakeBold(text)
    return text

  def AssertInitialization(self, clsname):
    if not self._widget:
      raise BuildException('%s was not correctly initialized' % clsname)

  def __str__(self):
    return str(self._action)

  @abstractmethod
  def GetValue(self):
    ''' Returns the state of the given widget '''
    pass

  def Update(self, size):
    '''
    Manually word wraps the StaticText help objects which would
    otherwise not wrap on resize

    Content area is based on each grid having two equally sized
    columns, where the content area is defined as 87% of the halved
    window width. The wiggle room is the distance +- 10% of the
    content_area.

    Wrap calculation is run only when the size of the help_msg
    extends outside of the wiggle_room. This was done to avoid
    the "flickering" that comes from constantly resizing a
    StaticText object.
    '''
    if self._msg is None:
      return
    help_msg = self._msg
    width, height = size
    content_area = int((width / 2) * .87)

    print 'wiget size', help_msg.Size[0]
    wiggle_room = range(int(content_area - content_area * .05), int(content_area + content_area * .05))
    print '(', int(content_area - content_area * .05), ' -> ', int(content_area + content_area * .05), ')'
    if help_msg.Size[0] not in wiggle_room:
      self._msg.SetLabel(self._msg.GetLabelText().replace('\n', ' '))
      self._msg.Wrap(content_area)


class Positional(AbstractComponent):
  """
  Represents a positional argument in a program
  e.g.
    mypyfile.py param1 <-- this guy
  """
  def __init__(self, action):
    self._action = action
    self._widget = None
    self.contents = None

  def BuildInputWidget(self, parent, action):
    return wx.TextCtrl(parent)

  def GetValue(self):
    '''
    Positionals have no associated options_string,
    so only the supplied arguments are returned.
    The order is assumed to be the same as the order
    of declaration in the client code

    Returns
      "argument_value"
    '''
    self.AssertInitialization('Positional')
    if str(self._widget.GetValue()) == EMPTY:
      return None
    return self._widget.GetValue()


class Choice(AbstractComponent):
  """ A dropdown box """

  _DEFAULT_VALUE = 'Select Option'

  def __init__(self, action):
    self._action = action
    self._widget = None
    self.contents = None

  def GetValue(self):
    '''
    Returns
      "--option_name argument"
    '''
    self.AssertInitialization('Choice')
    if self._widget.GetValue() == self._DEFAULT_VALUE:
      return None
    return ' '.join(
      [self._action.option_strings[0],  # get the verbose copy if available
       self._widget.GetValue()])

  def BuildInputWidget(self, parent, action):
    return wx.ComboBox(
        parent=parent,
        id=-1,
        value=self._DEFAULT_VALUE,
        choices=action.choices,
        style=wx.CB_DROPDOWN
    )


class Optional(AbstractComponent):
  def __init__(self, action):
    self._action = action
    self._widget = None
    self.contents = None

  def BuildInputWidget(self, parent, action):
    return wx.TextCtrl(parent)

  def GetValue(self):
    '''
    General options are key/value style pairs (conceptually).
    Thus the name of the option, as well as the argument to it
    are returned
    e.g.
      >>> myscript --outfile myfile.txt
    returns
      "--Option Value"
    '''
    self.AssertInitialization('Optional')
    value = self._widget.GetValue()
    if not value:
      return None
    return ' '.join(
      [self._action.option_strings[0],  # get the verbose copy if available
       value])


class Flag(AbstractComponent):
  def __init__(self, action):
    self._action = action
    self._widget = None
    self.contents = None

  def Build(self, parent):
    self._widget = self.BuildInputWidget(parent, self._action)
    self._msg = (self.CreateHelpMsgWidget(parent, self._action)
                 if self.HasHelpMsg(self._action)
                 else None)

    sizer = wx.BoxSizer(wx.VERTICAL)
    sizer.Add(self.CreateNameLabelWidget(parent, self._action))
    sizer.AddSpacer(6)

    if self.HasNargs(self._action):
      sizer.Add(self.CreateNargsMsg(parent, self._action))

    if self._msg:
      hsizer = self.buildHorizonalMsgSizer(parent)
      sizer.Add(hsizer, 1, wx.EXPAND)
    else:
      sizer.AddStretchSpacer(1)
      sizer.Add(self._widget, 0, wx.EXPAND)
    return sizer

  def BuildInputWidget(self, parent, action):
    return wx.CheckBox(parent, -1, label='')

  def buildHorizonalMsgSizer(self, panel):
    if not self._msg:
      return None
    sizer = wx.BoxSizer(wx.HORIZONTAL)
    sizer.Add(self._widget, 0)
    sizer.AddSpacer(6)
    sizer.Add(self._msg, 1, wx.EXPAND)
    return sizer

  def GetValue(self):
    '''
    Flag options have no param associated with them.
    Thus we only need the name of the option.
    e.g
      >>> Python -v myscript
    returns
      Options name for argument (-v)
    '''
    if self._widget.GetValue():
      return self._action.option_strings[0]

  def Update(self, size):
    '''
    Custom wrapper calculator to account for the
    increased size of the _msg widget after being
    inlined with the wx.CheckBox
    '''
    if self._msg is None:
      return
    help_msg = self._msg
    width, height = size
    content_area = int((width / 3) * .70)

    wiggle_room = range(int(content_area - content_area * .05), int(content_area + content_area * .05))
    if help_msg.Size[0] not in wiggle_room:
      self._msg.SetLabel(self._msg.GetLabelText().replace('\n', ' '))
      self._msg.Wrap(content_area)


class Counter(AbstractComponent):
  def __init__(self, action):
    self._action = action
    self._widget = None
    self.contents = None

  def BuildInputWidget(self, parent, action):
    levels = [str(x) for x in range(1, 7)]
    return wx.ComboBox(
      parent=parent,
      id=-1,
      value='',
      choices=levels,
      style=wx.CB_DROPDOWN
    )

  def GetValue(self):
    '''
    NOTE: Added on plane. Cannot remember exact implementation
    of counter objects. I believe that they count sequentail
    pairings of options
    e.g.
      -vvvvv
    But I'm not sure. That's what I'm going with for now.

    Returns
      str(action.options_string[0]) * DropDown Value
    '''
    dropdown_value = self._widget.GetValue()
    if not str(dropdown_value).isdigit():
      return None
    arg = str(self._action.option_strings[0]).replace('-', '')
    repeated_args = arg * int(dropdown_value)
    return '-' + repeated_args


if __name__ == '__main__':
  pass





