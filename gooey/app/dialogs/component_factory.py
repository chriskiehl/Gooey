'''
Created on Dec 8, 2013

@author: Chris
'''

import itertools
import components 
import action_sorter
import argparse_test_data


class ComponentFactory(object):
	'''
	Aggregates all of the actions and  
	'''
	
	def __init__(self, sorted_actions):
		
		self._actions = sorted_actions
		
		self.required_args		= self.BuildPositionals(self._actions)
		self.flags		 				= self.BuildFlags(self._actions)
		self.general_options	= (self.BuildChoices(self._actions)  
														+ self.BuildOptionals(self._actions)   
														+ self.BuildCounters(self._actions))
		
	def BuildPositionals(self, actions):
		return self._AssembleWidgetsFromActions(actions, 'Positional', '_positionals')
		
	def BuildChoices(self, actions):
		return self._AssembleWidgetsFromActions(actions, 'Choice', '_choices')
	
	def BuildOptionals(self, actions):
		return self._AssembleWidgetsFromActions(actions, 'Optional', '_optionals')
	
	def BuildFlags(self, actions):
		return self._AssembleWidgetsFromActions(actions, 'Flag', '_flags')
	
	def BuildCounters(self, actions):
		return self._AssembleWidgetsFromActions(actions, 'Counter', '_counters')
		
	def _AssembleWidgetsFromActions(self, actions, classname, actiontype):
		cls = getattr(components, classname)
		actions_list = getattr(actions, actiontype)
		return [cls(action)
					for action in actions_list]
		
	def __iter__(self):
		''' 
		return an iterator for all of the contained components
		'''
		return itertools.chain(self.required_args, 
													self.flags, 
													self.general_options)

if __name__ == '__main__':
	a = ComponentFactory(argparse_test_data.parser) 
				
				
				
				
				
