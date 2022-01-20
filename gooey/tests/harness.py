from contextlib import contextmanager

import time
from threading import Thread
from typing import Tuple

import wx

from gooey.gui import bootstrap
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
        frame.Destroy()
        del frame
