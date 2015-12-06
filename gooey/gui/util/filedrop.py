import wx

class FileDrop(wx.FileDropTarget):
  def __init__(self, window):
    wx.FileDropTarget.__init__(self)
    self.window = window

  def OnDropFiles(self, x, y, filenames):
    for name in filenames:
      self.window.WriteText(name)
