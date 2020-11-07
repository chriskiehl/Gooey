from contextlib import contextmanager

import time
from threading import Thread

import wx

from gooey.gui import application
from python_bindings.config_generator import create_from_parser
from python_bindings.gooey_decorator import defaults
from util.functional import merge




@contextmanager
def instrumentGooey(parser, **kwargs):
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
    buildspec = create_from_parser(parser, "", **merge(defaults, kwargs))
    app, gooey = application._build_app(buildspec, app)
    app.SetTopWindow(gooey)
    try:
        yield (app, gooey)
    finally:
        wx.CallAfter(app.ExitMainLoop)
        gooey.Destroy()
        app.SetTopWindow(None)
        del gooey
