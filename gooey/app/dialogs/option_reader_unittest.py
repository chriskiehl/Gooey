'''
Created on Jan 26, 2014

@author: Chris
'''

import types 
import unittest
from option_reader import OptionReader

	
class FakeClassWithoutImplementation(OptionReader):
	def __init__(self):
		pass 
	
class FakeClassWithImplementation(OptionReader):
	def __init__(self):
		pass 
	def GetOptions(self):
		pass
	
	
class Test(unittest.TestCase):
	
	def test_mixin_classes_throws_typeerror_without_implementation(self):
		with self.assertRaises(TypeError):
			fake_class = FakeClassWithoutImplementation() 
			
	def test_mixin_classes_passes_with_implementation(self):
		fc = FakeClassWithImplementation()
		

if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()