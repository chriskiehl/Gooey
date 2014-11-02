__author__ = 'Chris'

import wx
from wx.lib.scrolledpanel import ScrolledPanel


class TestPanel(ScrolledPanel):
  def __init__(self, parent):
    ScrolledPanel.__init__(self, parent)
    self.SetupScrolling(scroll_x=False)

    self.textctrls = [wx.TextCtrl(self) for _ in range(4)]

    sizer = wx.BoxSizer(wx.VERTICAL)
    hsizer = wx.BoxSizer(wx.HORIZONTAL)
    for textctrl in self.textctrls:
      hsizer.Add(textctrl, 1, wx.EXPAND)

    sizer.Add(hsizer, 0, wx.EXPAND)
    self.SetSizer(sizer)

class MyFrame(wx.Frame):
  def __init__(self, parent):
    wx.Frame.__init__(self, parent, title="test", size=(320, 240))
    self.SetBackgroundColour('#ffffff')
    self.panel = TestPanel(self)
    self.Show()

if __name__ == '__main__':
  app = wx.App(False)
  MyFrame(None)
  app.MainLoop()




  # a = {
  #   'required' : [
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

