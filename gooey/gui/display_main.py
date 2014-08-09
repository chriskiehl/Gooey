'''
Created on Dec 8, 2013

@author: Chris
'''

import os
import sys
import threading

import wx

from app.dialogs.controller import Controller
from app.images import image_store
from app.dialogs.header import FrameHeader
from app.dialogs.basic_config_panel import RuntimeDisplay
from app.dialogs.footer import Footer


class MessagePump(object):
  def __init__(self, queue):
    self.queue = queue
    self.stdout = sys.stdout

  # Overrides stdout's write method
  def write(self, text):
    if text != '':
      self.queue.put(text)


class Listener(threading.Thread):
  def __init__(self, queue, textbox):
    threading.Thread.__init__(self)
    self.queue = queue
    self.update_text = lambda x: textbox.AppendText(x)

  def run(self):
    while True:
      try:
        stdout_msg = self.queue.get(timeout=1)
        if stdout_msg != '':
          self.update_text(stdout_msg)
      except Exception as e:
        pass  # Timeout. Aint nobody care 'bout dat


class MainWindow(wx.Frame):
  def __init__(self, queue, payload=None):
    wx.Frame.__init__(
      self,
      parent=None,
      id=-1,
      title=os.path.basename(__file__),
      size=(640, 480)
    )

    self._controller = Controller()

    self._init_properties()
    self._init_components()
    self._do_layout()

    self.queue = queue
    # the client's main function
    self._payload = payload

    _stdout = sys.stdout
    sys.stdout = MessagePump(queue)
    listener = Listener(queue, self.config_panel.cmd_textbox)
    listener.start()

  def _init_properties(self):
    self.SetMinSize((400, 300))
    self.icon = wx.Icon(image_store.icon, wx.BITMAP_TYPE_ICO)
    self.SetIcon(self.icon)

  def _init_components(self):
    # init gui
    self.head_panel = FrameHeader(image_path=image_store.computer3, parent=self, size=(30, 90))
    self.config_panel = RuntimeDisplay(parent=self)
    self.foot_panel = Footer(self, self._controller)

  def _do_layout(self):
    sizer = wx.BoxSizer(wx.VERTICAL)
    sizer.Add(self.head_panel, 0, wx.EXPAND)
    self._draw_horizontal_line(sizer)
    sizer.Add(self.config_panel, 1, wx.EXPAND)
    self._draw_horizontal_line(sizer)
    sizer.Add(self.foot_panel, 0, wx.EXPAND)
    self.SetSizer(sizer)

  def _init_panels(self):
    self._frame_header = FrameHeader
    self._basic_config_body = None
    self._adv_config_body = None
    self._config_footer = None
    self._output_footer = None

  def _draw_horizontal_line(self, sizer):
    line = wx.StaticLine(self, -1, style=wx.LI_HORIZONTAL)
    line.SetSize((10, 10))
    sizer.Add(line, 0, wx.EXPAND)
		
		
		
		
		
		
		
		
		