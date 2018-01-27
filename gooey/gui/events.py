"""
App wide event registry

Everything in the application is communicated via pubsub. These are the events
that tie everything together.
"""

import wx

WINDOW_STOP     = wx.NewId()
WINDOW_CANCEL   = wx.NewId()
WINDOW_CLOSE    = wx.NewId()
WINDOW_START    = wx.NewId()
WINDOW_RESTART  = wx.NewId()
WINDOW_EDIT     = wx.NewId()

WINDOW_CHANGE   = wx.NewId()
PANEL_CHANGE    = wx.NewId()
LIST_BOX        = wx.NewId()

CONSOLE_UPDATE  = wx.NewId()
EXECUTION_COMPLETE = wx.NewId()
PROGRESS_UPDATE = wx.NewId()

USER_INPUT = wx.NewId()

