import wx
from wx.lib.pubsub import pub

from gooey.gui.util import wx_util


class Sidebar(wx.Panel):

  def __init__(self, parent, *args, **kwargs):
    self.contents = kwargs.pop('contents', [])
    super(Sidebar, self).__init__(parent, *args, **kwargs)
    self.SetDoubleBuffered(True)

    self._parent = parent

    self._controller = None

    self._init_components()
    self._do_layout()

  def _init_components(self):
    pass

  def _do_layout(self):
    self.SetDoubleBuffered(True)
    self.SetBackgroundColour('#f2f2f2')
    self.SetSize((180, 0))
    self.SetMinSize((180, 0))

    STD_LAYOUT = (0, wx.LEFT | wx.RIGHT | wx.EXPAND, 10)

    container = wx.BoxSizer(wx.VERTICAL)
    container.AddSpacer(15)
    container.Add(wx_util.H1(self, 'Actions'), *STD_LAYOUT)
    container.AddSpacer(5)
    thing = wx.ListBox(self, -1, choices=['Connect', 'process', 'commit', 'fetch'])
    container.Add(thing, 1, wx.LEFT | wx.RIGHT | wx.EXPAND, 10)
    container.AddSpacer(20)
    self.SetSizer(container)

    self.Bind(wx.EVT_LISTBOX, self.onClick, thing)

  def onClick(self, evt):
    pub.sendMessage("panelListener", message=evt.GetString())
    evt.Skip()
