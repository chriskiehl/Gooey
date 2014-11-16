from gooey.gui.widgets import components2

__author__ = 'Chris'

import unittest
import wx
from wx.lib.scrolledpanel import ScrolledPanel

TEXT_FIELD = components2.TextField({
  'display_name': 'cool title',
  'help_msg': 'a help message',
  'nargs': '+',
  'commands': ['-f', '--fudge'],
  'choices': []
})

DROPDOWN = components2.Dropdown({
  'display_name': 'cool title',
  'help_msg': 'a help message',
  'nargs': '+',
  'commands': ['-f', '--fudge'],
  'choices': ['one', 'two', 'three']
})

COUNTER = components2.Counter({
  'display_name': 'cool title',
  'help_msg': 'a help message',
  'nargs': '+',
  'commands': ['-f', '--fudge'],
  'choices': []
})

CHECKBOX = components2.CheckBox({
  'display_name': 'cool title',
  'help_msg': 'a help message',
  'nargs': '+',
  'commands': ['-f', '--fudge'],
  'choices': []
})

RADIOGROUP = components2.RadioGroup({
  'display_name': 'mutux options',
  'data': [{
    'help_msg': 'a help message',
    'nargs': '+',
    'commands': ['-f', '--fudge'],
    'choices': []
   }, {
    'help_msg': 'a help message',
    'nargs': '+',
    'commands': ['-g', '--gudge'],
    'choices': []
  }]
})


class TestPanel(ScrolledPanel):
  def __init__(self, parent, widget):
    ScrolledPanel.__init__(self, parent)
    self.SetupScrolling(scroll_x=False)

    sizer = wx.BoxSizer(wx.VERTICAL)
    self.widget = widget

    sizer.Add(self.widget.build(self), 0, wx.EXPAND)
    self.SetSizer(sizer)


class MyFrame(wx.Frame):
  def __init__(self, parent, widget):
    wx.Frame.__init__(self, parent, title="test", size=(320, 240))
    self.SetBackgroundColour('#ffffff')
    self.panel = TestPanel(self, widget)
    self.Show()

  def get_widget(self):
    return self.panel.widget

  def close(self):
    self.Destroy()



class TestComponents(unittest.TestCase):

  def setUp(self):
    self.app = wx.App(False)
    self.frame = None

  def tearDown(self):
    # self.app = wx.App(False)
    self.frame.Destroy()
    self.frame = None

  def test_textfield_returns_option_and_value_else_none(self):
    self.build_test_frame(TEXT_FIELD)
    self.assertTrue(self.get_value() == '')
    self.get_widget().SetLabelText('value')
    self.assertEqual('-f value', self.get_value())


  def test_dropdown_returns_option_and_value_else_none(self):
    self.build_test_frame(DROPDOWN)
    self.assertTrue(self.get_value() == '')
    # grab first item from the combo box
    self.frame.get_widget()._GetWidget().SetSelection(0)
    self.assertEqual('-f one', self.get_value())


  def test_counter_returns_option_and_value_else_none(self):
    self.build_test_frame(COUNTER)
    self.assertTrue(self.get_value() == '')
    # counter objects stack,
    # so
    #   1 = -f,
    #   4 = -ffff
    self.frame.get_widget()._GetWidget().SetSelection(0)
    self.assertEqual('-f', self.get_value())
    self.frame.get_widget()._GetWidget().SetSelection(4)
    self.assertEqual('-fffff', self.get_value())


  def test_checkbox_returns_option_if_checked_else_none(self):
    self.build_test_frame(CHECKBOX)
    self.assertTrue(self.get_value() == '')
    self.frame.get_widget()._GetWidget().SetValue(1)
    self.assertEqual('-f', self.get_value())


  def test_radiogroup_returns_option_if_checked_else_none(self):
    self.build_test_frame(RADIOGROUP)
    self.assertTrue(self.get_value() == '')
    # self.frame.get_widget()._GetWidget()[0].SetValue(1)
    # self.assertEqual('-f', self.get_value())


  def build_test_frame(self, widget):
    # self.app = wx.App(False)
    self.frame = MyFrame(None, widget)

  def get_widget(self):
    return self.frame.get_widget()._GetWidget()

  def get_value(self):
    return self.frame.get_widget().GetValue()



if __name__ == '__main__':
  unittest.main()




  # a = {
  # 'required' : [
  #     {
  #       'component': 'TextField',
  #       'data': {
  #         'display_name': 'filename',
  #         'help_text': 'path to file you want to process',
  #         'command_args': ['-f', '--infile']
  #       }
  #     },
  #     {
  #       'component': 'FileChooser',
  #       'data': {
  #         'display_name': 'Output Location',
  #         'help_text': 'Where to save the file',
  #         'command_args': ['-o', '--outfile']
  #       }
  #     }
  #   ],
  #   'optional' : [
  #     {
  #       'component': 'RadioGroup',
  #       'data': [
  #         {
  #           'display_name': 'Output Location',
  #           'help_text': 'Where to save the file',
  #           'command_args': ['-o', '--outfile']
  #         }, {
  #           'display_name': 'Output Location',
  #           'help_text': 'Where to save the file',
  #           'command_args': ['-o', '--outfile']
  #         }
  #       ]
  #     }
  #   ]
  # }
  #
  #   ]
  # }

