'''
Created on Jan 7, 2014

@author: Chris
'''

import wx 
import os
import sys
import unittest
import advanced_config
from argparse import ArgumentParser 

class Test(unittest.TestCase):


	def setUp(self):
		parser = ArgumentParser(description='Example Argparse Program')
		parser.add_argument("filename", help="Name of the file you want to read")
		parser.add_argument('-T', '--tester', choices=['yes','no'])
		parser.add_argument('-o', '--outfile', help='Redirects output to the specified file')
		parser.add_argument('-v', '--verbose', help='Toggles verbosity off')
		parser.add_argument('-e', '--repeat', action='count', help='Set the number of times to repeat')
		self.parser = parser 
		
	def buildWindow(self):
		app = wx.PySimpleApp()
		module_name = os.path.split(sys.argv[0])[-1]
		frame = wx.Frame(None, -1, module_name)

		panel = advanced_config.AdvancedConfigPanel(frame, self.parser)
		frame.Show()
		app.MainLoop()

	def testAdvancedConfigPanel(self):
		self.buildWindow()


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()