# '''
# Created on Jan 4, 2014
#
# @author: Chris
#
#
#
#
# '''
#
# import os
# import sys
# import unittest
# from argparse import ArgumentParser
#
# import wx
#
#
# class ComponentsTest(unittest.TestCase):
#   def setUp(self):
#     parser = ArgumentParser(description='Example Argparse Program')
#     parser.add_argument("filename", help="Name of the file you want to read")
#     parser.add_argument('-T', '--tester', choices=['yes', 'no'])
#     parser.add_argument('-o', '--outfile', help='Redirects output to the specified file')
#     parser.add_argument('-v', '--verbose', help='Toggles verbosity off')
#     parser.add_argument('-e', '--repeat', action='count')
#     action = parser._actions
#     self.actions = {
#       'help': action[0],
#       'Positional': action[1],
#       'Choice': action[2],
#       'Optional': action[3],
#       'Flag': action[4],
#       'Counter': action[5]
#     }
#
#
#   def BuildWindow(self, component, _type):
#     app = wx.PySimpleApp()
#     module_name = os.path.split(sys.argv[0])[-1]
#     frame = wx.Frame(None, -1, _type)
#
#     panel = wx.Panel(frame, -1, size=(320, 240))
#     component_sizer = component.Build(panel)
#     panel.SetSizer(component_sizer)
#
#     frame.Show(True)
#
#     app.MainLoop()
#
#
#   def testPositionalWidgetBuild(self):
#     self.SetupWidgetAndBuildWindow('Positional')
#
#   def testChoiceWidgetBuild(self):
#     self.SetupWidgetAndBuildWindow('Choice')
#
#   def testOptionalWidgetBuild(self):
#     self.SetupWidgetAndBuildWindow('Optional')
#
#   def testFlagWidgetBuild(self):
#     self.SetupWidgetAndBuildWindow('Flag')
#
#   def testCounterWidgetBuild(self):
#     self.SetupWidgetAndBuildWindow('Counter')
#
#   def SetupWidgetAndBuildWindow(self, _type):
#     component = getattr(components, _type)(self.actions[_type])
#     self.BuildWindow(component, _type)
#
#
# if __name__ == "__main__":
#   # import sys;sys.argv = ['', 'Test.testName']
#   unittest.main()
#
