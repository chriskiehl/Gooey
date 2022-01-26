'''
Main runner entry point for Gooey.
'''
from typing import Any, Tuple

import wx  # type: ignore
# wx.html and wx.xml imports required here to make packaging with
# pyinstaller on OSX possible without manually specifying `hidden_imports`
# in the build.spec
import wx.html  # type: ignore
import wx.lib.inspection  # type: ignore
import wx.richtext  # type: ignore
import wx.xml  # type: ignore

from gooey.gui import image_repository
from gooey.gui.application.application import RGooey
from gooey.gui.lang import i18n
from gooey.util.functional import merge
from rewx import render, create_element  # type: ignore


def run(build_spec):
    app, _ = build_app(build_spec)
    app.MainLoop()


def build_app(build_spec):
    app = wx.App(False)
    return _build_app(build_spec, app)


def _build_app(build_spec, app) -> Tuple[Any, wx.Frame]:
    """
    Note: this method is broken out with app as
    an argument to facilitate testing.
    """
    # use actual program name instead of script file name in macOS menu
    app.SetAppDisplayName(build_spec['program_name'])

    i18n.load(build_spec['language_dir'], build_spec['language'], build_spec['encoding'])
    imagesPaths = image_repository.loadImages(build_spec['image_dir'])
    gapp2 = render(create_element(RGooey, merge(build_spec, imagesPaths)), None)
    # wx.lib.inspection.InspectionTool().Show()
    # gapp.Show()
    gapp2.Show()
    return (app, gapp2)
