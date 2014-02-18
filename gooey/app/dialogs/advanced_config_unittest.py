'''
Created on Jan 7, 2014

@author: Chris
'''

import wx 
import os
import sys
import unittest
import advanced_config
import argparse_test_data
from argparse import ArgumentParser 
from gooey_decorator.app.dialogs.config_model import ConfigModel

class TestAdvancedConfigPanel(unittest.TestCase):

	def setUp(self):
		self.parser = argparse_test_data.parser 
		
	def buildWindow(self):
		app = wx.PySimpleApp()
		module_name = os.path.split(sys.argv[0])[-1]
		frame = wx.Frame(None, -1, module_name, size=(640,480))
		
		panel = advanced_config.AdvancedConfigPanel(frame, ConfigModel(self.parser))
		frame.Show()
		app.MainLoop()

	def testAdvancedConfigPanel(self):
		self.buildWindow()


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()
	
	
	
	
	
	
	
	
	
	