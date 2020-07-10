"""
App wide event registry

Everything in the application is communicated via pubsub. These are the events
that tie everything together.
"""

import wx

WINDOW_STOP     = wx.Window.NewControlId()
WINDOW_CANCEL   = wx.Window.NewControlId()
WINDOW_CLOSE    = wx.Window.NewControlId()
WINDOW_START    = wx.Window.NewControlId()
WINDOW_RESTART  = wx.Window.NewControlId()
WINDOW_EDIT     = wx.Window.NewControlId()

WINDOW_CHANGE   = wx.Window.NewControlId()
PANEL_CHANGE    = wx.Window.NewControlId()
LIST_BOX        = wx.Window.NewControlId()

CONSOLE_UPDATE  = wx.Window.NewControlId()
EXECUTION_COMPLETE = wx.Window.NewControlId()
PROGRESS_UPDATE = wx.Window.NewControlId()
TIME_UPDATE    = wx.Window.NewControlId()

USER_INPUT = wx.Window.NewControlId()

LEFT_DOWN = wx.Window.NewControlId()

