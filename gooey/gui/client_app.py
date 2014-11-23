'''
Created on Jan 23, 2014

@author: Chris
'''

import sys

from gooey.gui.action_sorter import ActionSorter


class ClientApp(object):
  def __init__(self, parser, payload):
    self._parser = parser
    self.description = parser.description
    self.action_groups = ActionSorter(self._parser._actions)
    self.payload = payload

  def HasPositionals(self):
    if self.action_groups._positionals:
      return True
    return False

  def IsValidArgString(self, arg_string):
    if isinstance(self._Parse(arg_string), str):
      return False
    return True

  def _Parse(self, arg_string):
    try:
      self._parser.parse_args(arg_string.split())
      return True
    except Exception as e:
      return str(e)

  def GetErrorMsg(self, arg_string):
    return self._FormatMsg(self._Parse(arg_string))

  def _FormatMsg(self, msg):
    output = list(msg)
    if ':' in output:
      output[output.index(':')] = ':\n '
    return ''.join(output)

  def AddToArgv(self, arg_string):
    sys.argv.extend(arg_string.split())


class EmptyClientApp(object):
  def __init__(self, payload):
    '''
    initializes a BlankModel object

    As you can see. This class does nothing..
    '''

    self.description = ''
    self.payload = payload


if __name__ == '__main__':
  pass

