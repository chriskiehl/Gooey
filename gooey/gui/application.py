'''
Main runner entry point for Gooey.
'''

import wx
# wx.html and wx.xml imports required here to make packaging with
# pyinstaller on OSX possible without manually specifying `hidden_imports`
# in the build.spec
import wx.html
import wx.xml
import wx.richtext  # Need to be imported before the wx.App object is created.
import wx.lib.inspection
from gooey.gui.lang import i18n

from gooey.gui import image_repository
from gooey.gui.containers.application import GooeyApplication
from gooey.util.functional import merge


def run(build_spec):
    app, _ = build_app(build_spec)
    app.MainLoop()


def build_app(build_spec):
    app = wx.App(False)
    return _build_app(build_spec, app)


def _build_app(build_spec, app):
    """
    Note: this method is broken out with app as
    an argument to facilitate testing.
    """
    # use actual program name instead of script file name in macOS menu
    app.SetAppDisplayName(build_spec['program_name'])

    i18n.load(build_spec['language_dir'], build_spec['language'], build_spec['encoding'])
    imagesPaths = image_repository.loadImages(build_spec['image_dir'])
    gapp = GooeyApplication(merge(build_spec, imagesPaths))
    # wx.lib.inspection.InspectionTool().Show()
    gapp.Show()
    return (app, gapp)
