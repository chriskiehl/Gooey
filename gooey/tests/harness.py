from contextlib import contextmanager

import wx

from gui import application
from python_bindings.config_generator import create_from_parser
from python_bindings.gooey_decorator import defaults
from util.functional import merge


@contextmanager
def instrumentGooey(parser, **kwargs):
    """
    Context manager used during testing for setup/tear down of the
    WX infrastructure during subTests.
    """
    buildspec = create_from_parser(parser, "", **merge(defaults, kwargs))
    app, gooey = application.build_app(buildspec)
    try:
        yield (app, gooey)
    finally:
        wx.CallAfter(app.ExitMainLoop)
        app.Destroy()