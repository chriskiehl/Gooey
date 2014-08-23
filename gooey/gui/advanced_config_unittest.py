'''
Created on Jan 7, 2014

@author: Chris
'''

import os
import sys
import unittest

import wx

import advanced_config
from gooey.gui.client_app import ClientApp
from gooey.gui import argparse_test_data


class TestAdvancedConfigPanel(unittest.TestCase):
  def setUp(self):
    self.parser = argparse_test_data.parser

  def buildWindow(self):
    app = wx.PySimpleApp()
    module_name = os.path.split(sys.argv[0])[-1]
    frame = wx.Frame(None, -1, module_name, size=(640, 480))

    panel = advanced_config.AdvancedConfigPanel(frame, ClientApp(self.parser))
    frame.Show()
    app.MainLoop()

  def testAdvancedConfigPanel(self):
    self.buildWindow()


if __name__ == "__main__":
  #import sys;sys.argv = ['', 'Test.testName']
  unittest.main()
	
	
	
	
	
	
	
	
	
	