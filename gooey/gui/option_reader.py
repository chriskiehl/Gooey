'''
Created on Jan 19, 2014

@author: Chris
'''
from builtins import object

from abc import ABCMeta, abstractmethod
from future.utils import with_metaclass


class OptionReader(with_metaclass(ABCMeta, object)):
  '''
  Mixin for forcing subclasses to
  honor GetOptions method
  '''

  @abstractmethod
  def GetOptions(self):
    '''
    Implemented by subclasses.
    Defines how the config panel Views retrieve their options
    '''
    pass