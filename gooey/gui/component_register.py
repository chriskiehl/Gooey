'''
Created on Jan 20, 2014

@author: Chris
'''


class ComponentRegister(object):
  ''' Mixin class for attaching controllers to objects '''

  def Registercontroller(self, controller):
    ''' Assigns a Controller to a view (usually panel or frame) object'''
    if self._controller in None:
      self._controller = controller