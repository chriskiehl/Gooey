from collections import defaultdict

__ALL__ = ['pub']

class PubSub(object):
  '''
  A super simplified clone of Wx.lib.pubsub since it doesn't exist on linux

  *grumble grumble* Stupid abandoned wx project... >:(  *grumble*
  '''

  def __init__(self):
    self.registry = defaultdict(list)


  def subscribe(self, handler, event):
    self.registry[event].append(handler)


  def send_message(self, event, **kwargs):
    for event_handler in self.registry.get(event, []):
      event_handler(**kwargs)

pub = PubSub()

