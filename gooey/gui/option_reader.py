'''
Created on Jan 19, 2014

@author: Chris
'''

from abc import ABCMeta, abstractmethod


class OptionReader(object):
  '''
  Mixin for forcing subclasses to
  honor GetOptions method
  '''
  __metaclass__ = ABCMeta

  @abstractmethod
  def GetOptions(self):
    '''
    Implemented by subclasses.
    Defines how the config panel Views retrieve their options
    '''
    pass