'''
Created on Jan 25, 2014

@author: Chris
'''

from i18n import I18N
import unittest


class Test(unittest.TestCase):


	def setUp(self):
		pass

	def testI18nThrowsIOErrorOnBadPath(self):
		with self.assertRaises(IOError):
			I18N('franch')
		


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()