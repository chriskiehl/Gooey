import wx


class FileDrop(wx.FileDropTarget):
    def __init__(self, window, dropStrategy=None):
        wx.FileDropTarget.__init__(self)
        self.window = window
        self.dropHandler = dropStrategy or self._defaultStrategy

    def OnDropFiles(self, x, y, filenames):
        return self.dropHandler(x, y, filenames)

    def _defaultStrategy(self, x, y, filenames):
        for name in filenames:
            self.window.WriteText(name)
        return True
