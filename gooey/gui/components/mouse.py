"""
WxPython lacks window level event hooks. Meaning, there's no
general way to subscribe to every mouse event that goes on within
the application.

To implement features which respond to clicks outside of their
immediate scope, for instance, dropdowns, a workaround in the form
of manually binding all mouse events, for every component, to a single
top level handler needs to be done.

Normally, this type of functionality would be handled by wx.PopupTransientWindow.
However, there's a long standing bug with it and the ListBox/Ctrl
classes which prevents its usage and thus forcing this garbage.

See: https://github.com/wxWidgets/Phoenix/blob/705aa63d75715f8abe484f4559a37cb6b09decb3/demo/PopupWindow.py
"""


from gooey.gui.pubsub import pub
import gooey.gui.events as events

def notifyMouseEvent(event):
    """
    Notify interested listeners of the LEFT_DOWN mouse event
    """
    # TODO: is there ever a situation where this wouldn't be skipped..?
    event.Skip()
    pub.send_message_sync(events.LEFT_DOWN, wxEvent=event)