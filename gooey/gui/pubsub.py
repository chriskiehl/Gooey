import wx
from collections import defaultdict

__ALL__ = ['pub']


class PubSub(object):
    """
    A super simplified clone of Wx.lib.pubsub since it doesn't exist on linux
    """

    def __init__(self):
        self.registry = defaultdict(list)

    def subscribe(self, event, handler):
        self.registry[event].append(handler)

    def send_message(self, event, **kwargs):
        for event_handler in self.registry.get(event, []):
            wx.CallAfter(event_handler, **kwargs)

    def send_message_sync(self, event, **kwargs):
        """
        ===== THIS IS NOT THREAD SAFE =====
        Synchronously sends the message to all relevant consumers
        and blocks until a response is received.

        This MUST ONLY be used for communication within
        the same thread! It exists primarily as an escape
        hatch for bubbling up messages (which would be garbage
        collected in the CallAfter form) to interested components
        """
        for event_handler in self.registry.get(event, []):
            event_handler(**kwargs)

pub = PubSub()
