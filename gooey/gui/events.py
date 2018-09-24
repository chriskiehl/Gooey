"""
App wide event registry

Everything in the application is communicated via pubsub. These are the events
that tie everything together.
"""

import wx

WINDOW_STOP     = wx.NewIdRef()
WINDOW_CANCEL   = wx.NewIdRef()
WINDOW_CLOSE    = wx.NewIdRef()
WINDOW_START    = wx.NewIdRef()
WINDOW_RESTART  = wx.NewIdRef()
WINDOW_EDIT     = wx.NewIdRef()

WINDOW_CHANGE   = wx.NewIdRef()
PANEL_CHANGE    = wx.NewIdRef()
LIST_BOX        = wx.NewIdRef()

CONSOLE_UPDATE  = wx.NewIdRef()
EXECUTION_COMPLETE = wx.NewIdRef()
PROGRESS_UPDATE = wx.NewIdRef()

USER_INPUT = wx.NewIdRef()
