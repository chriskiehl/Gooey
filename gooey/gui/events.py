"""
App wide event registry

Everything in the application is communitcated via pubsub. These are the events that
tie everythign together.
"""
import wx

new_id = lambda: str(wx.NewId())

WINDOW_STOP     = new_id()
WINDOW_CANCEL   = new_id()
WINDOW_CLOSE    = new_id()
WINDOW_START    = new_id()
WINDOW_RESTART  = new_id()
WINDOW_EDIT     = new_id()

WINDOW_CHANGE   = new_id()
PANEL_CHANGE    = new_id()
