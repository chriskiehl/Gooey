from contextlib import contextmanager

import wx

from gooey.gui import application
from gooey.python_bindings.config_generator import create_from_parser
from gooey.python_bindings.gooey_decorator import defaults
from gooey.util.functional import merge


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
        gooey.Destroy()
        app.Destroy()
