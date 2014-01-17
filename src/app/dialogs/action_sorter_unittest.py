'''
Created on Jan 16, 2014

@author: Chris
'''

import time
import unittest
import argparse_test_data
from functools import partial
from argparse import _StoreAction, _HelpAction
from action_sorter import ActionSorter

class Test(unittest.TestCase):


	def setUp(self):
		self._actions = argparse_test_data.parser._actions
		self.sorted_actions = ActionSorter(self._actions)
		# pain in the A... PEP8 be damned! 
		self.expected_positionals = [
						"_StoreAction(option_strings=[], dest='filename', nargs=None, const=None, default=None, type=None, choices=None, help='Name of the file you want to read', metavar=None)",
						'''_StoreAction(option_strings=[], dest='outfile', nargs=None, const=None, default=None, type=None, choices=None, help="Name of the file where you'll save the output", metavar=None)'''												
						]
		self.expected_choices = [
						'''_StoreAction(option_strings=['-T', '--tester'], dest='tester', nargs=None, const=None, default=None, type=None, choices=['yes', 'no'], help="Yo, what's up man? I'm a help message!", metavar=None)'''
						]
		self.expected_optionals = [
						'''_StoreAction(option_strings=['-o', '--outfile'], dest='outfile', nargs=None, const=None, default=None, type=None, choices=None, help='Redirects output to the file specified by you, the awesome user', metavar=None)''',
						'''_StoreAction(option_strings=['-v', '--verbose'], dest='verbose', nargs=None, const=None, default=None, type=None, choices=None, help='Toggles verbosity off', metavar=None)''',
						'''_StoreAction(option_strings=['-s', '--schimzammy'], dest='schimzammy', nargs=None, const=None, default=None, type=None, choices=None, help='Add in an optional shimzammy parameter', metavar=None)'''								
						]
		self.expected_counters = [
						'''_CountAction(option_strings=['-e', '--repeat'], dest='repeat', nargs=0, const=None, default=None, type=None, choices=None, help='Set the number of times to repeat', metavar=None)'''
						]
		
		self.expected_flags = [
						'''_StoreConstAction(option_strings=['-c', '--constoption'], dest='constoption', nargs=0, const='myconstant', default=None, type=None, choices=None, help='Make sure the const action is correctly sorted', metavar=None)''',
						'''_StoreTrueAction(option_strings=['-t', '--truify'], dest='truify', nargs=0, const=True, default=False, type=None, choices=None, help='Ensure the store_true actions are sorted', metavar=None)''',
						'''_StoreFalseAction(option_strings=['-f', '--falsificle'], dest='falsificle', nargs=0, const=False, default=True, type=None, choices=None, help='Ensure the store_false actions are sorted', metavar=None)'''							
						]

	def testPositionalsReturnsOnlyPositionalActions(self):
		positionals = self.sorted_actions._positionals
		self.assertEqual(len(positionals), 2)
		
		self.assertForAllActionsInList(positionals,self.expected_positionals)
			
	def testHelpActionNotInOptionals(self):
		_isinstance = lambda x: isinstance(x, _HelpAction)
		self.assertFalse(any(map(_isinstance, self.sorted_actions._optionals)))
		
	def testChoicesOnlyReturnsChoices(self):
		self.assertForAllActionsInList(self.sorted_actions._choices,
																	self.expected_choices)
		
	def testOptionalsOnlyReturnsOptionals(self):
		self.assertForAllActionsInList(self.sorted_actions._optionals,
																	self.expected_optionals)
		
	def testCounterSortOnlyReturnsCounters(self):
		self.assertForAllActionsInList(self.sorted_actions._counters,
																	self.expected_counters)
		
	def testFlagSortReturnsOnlyFlags(self):
		self.assertForAllActionsInList(self.sorted_actions._flags,
																	self.expected_flags)
	
	def assertForAllActionsInList(self, actions, expected_actions):
		for index, action in enumerate(actions):
			self.assertEqual(str(action), expected_actions[index])
			
	

		
		

if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()