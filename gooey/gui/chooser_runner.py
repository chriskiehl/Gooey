__author__ = 'Chris'

import wx

from gooey.gui.widgets.choosers import CalendarChooser


class MyFrame(wx.Frame):
  def __init__(self, parent):
    wx.Frame.__init__(self, parent, title="test", size=(320, 240))
    self.SetBackgroundColour('#ffffff')

    sizer = wx.BoxSizer(wx.VERTICAL)
    f = wx.FileDialog(self, style=wx.FD_MULTIPLE | wx.FD_FILE_MUST_EXIST)
    sizer.Add(f, 0, wx.EXPAND)
    self.SetSizer(sizer)

if __name__ == '__main__':
  app = wx.App(False)
  frame = MyFrame(None)
  frame.Show(True)
  app.MainLoop()



