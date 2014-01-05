'''
Created on Jan 4, 2014

@author: Chris




'''

import wx
import os 
import sys
import unittest
import components
from argparse import ArgumentParser


class ComponentsTest(unittest.TestCase):
	
	def setUp(self):
		parser = ArgumentParser(description='Example Argparse Program')
		parser.add_argument("filename", help="Name of the file you want to read")
		parser.add_argument('-T', '--tester', choices=['yes','no'])
		action = parser._actions
		self.actions = {
					'help' : action[0],
					'Positional' : action[1],
					'Choice' : action[2]				
					}
		

	def BuildWindow(self, component):
		
		app = wx.PySimpleApp()
		module_name = os.path.split(sys.argv[0])[-1]
		frame = wx.Frame(None, -1, module_name)
		
		panel = wx.Panel(frame, -1, size=(320,240))
		component_sizer = component.Build(panel)
		panel.SetSizer(component_sizer)
		
		frame.Show(True)
		
		print component.GetValue()
		app.MainLoop()
		
	def testPositionalWidgetBuild(self):
		self.SetupWidgetAndBuildWindow('Positional')
# 		component = components.Positional(self.actions['positional'])
# 		self.BuildWindow(component)
		
	def testChoiceWidgetBuild(self):
		self.SetupWidgetAndBuildWindow('Choice')
		
	def SetupWidgetAndBuildWindow(self, _type):
		component = getattr(components, _type)(self.actions[_type])
		self.BuildWindow(component)
		

if __name__ == "__main__":
	# import sys;sys.argv = ['', 'Test.testName']
	unittest.main()
	
	
	
	
	
	
	
	
