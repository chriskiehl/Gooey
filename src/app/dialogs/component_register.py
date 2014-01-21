'''
Created on Jan 20, 2014

@author: Chris
'''

class ComponentRegister(object):

	def __init__(self, params):
		pass 
	
	def Registercontroller(self, controller):
		if self._controller in None: 
			self._controller = controller