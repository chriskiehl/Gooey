import wx
from collections import defaultdict

__ALL__ = ['pub']

class PubSub(object):
  '''
  A super simplified clone of Wx.lib.pubsub since it doesn't exist on linux
  '''

  def __init__(self):
    self.registry = defaultdict(list)


  def subscribe(self, event, handler):
    self.registry[event].append(handler)


  def send_message(self, event, **kwargs):
    for event_handler in self.registry.get(event, []):
      wx.CallAfter(event_handler, **kwargs)

pub = PubSub()

