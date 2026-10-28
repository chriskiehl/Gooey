from contextlib import contextmanager

import importlib
import time
from threading import Thread
from typing import Tuple

import wx
from rewx import widgets

from gooey.gui import bootstrap
from gooey.gui import events
from gooey.python_bindings.config_generator import create_from_parser
from gooey.python_bindings.parameters import gooey_params
from gooey.util.functional import merge
from gooey.gui.application.application import RGooey


@contextmanager
def instrumentGooey(parser, **kwargs) -> Tuple[wx.App, wx.Frame, RGooey]:
    """
    Context manager used during testing for setup/tear down of the
    WX infrastructure during subTests.

    Weirdness warning: this uses a globally reused wx.App instance.
    """
    from gooey.tests import app
    if app == None:
        raise Exception("App instance has not been created! This is likely due to "
                        "you forgetting to add the magical import which makes all these "
                        "tests work. See the module doc in gooey.tests.__init__ for guidance")
    # wx frees a window's control ids when it is destroyed, so give each test
    # window fresh event ids, as a new run of the program would get.
    importlib.reload(events)
    buildspec = create_from_parser(parser, "", **gooey_params(**kwargs))
    app, frame = bootstrap._build_app(buildspec, app)
    app.SetTopWindow(frame)
    try:
        # we need to run the main loop temporarily to get it to
        # apply any pending updates from the initial creation.
        # The UI state will be stale otherwise
        # this works because CallLater just enqueues the message to
        # be processed. The MainLoop starts running, picks it up, and
        # then exists
        wx.CallLater(1, app.ExitMainLoop)
        app.MainLoop()
        yield (app, frame, frame._instance)
    finally:
        # re-wx keeps the macOS dock icon on its frame widget function rather
        # than on the window, so destroy it here to let the next test create one.
        taskbar_icon = getattr(widgets.frame, 'taskbarIcon', None)
        if taskbar_icon is not None:
            taskbar_icon.Destroy()
            widgets.frame.taskbarIcon = None
        frame._instance.timer.stop()
        frame.Destroy()
        app.Yield(True)
        del frame
