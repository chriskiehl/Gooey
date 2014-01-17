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
	Aggregates all of the Widgets and dispatches 
	them to the caller.   
	'''
	
	def __init__(self, parser):
		
		self._actions = action_sorter.ActionSorter(parser._actions[:])
		
		self.positionals	= self.BuildPositionals(self._actions)
		self.choices			= self.BuildChoices(self._actions)
		self.optionals 		= self.BuildOptionals(self._actions) 
		self.flags		 		= self.BuildFlags(self._actions)
		self.counters 		= self.BuildCounters(self._actions)
		
		self._components = [
										self.positionals,
										self.choices,
										self.optionals,
										self.flags,
										self.counters				
										]
		
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
		
# 	def __getitem__(self, slice):
# 		return self._components[slice] 

	def __iter__(self):
		''' 
		return an iterator for all of the contained 
		components
		'''
		return itertools.chain(*self._components)

if __name__ == '__main__':
	a = ComponentFactory(argparse_test_data.parser) 
				
				
				
				
				
