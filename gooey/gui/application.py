'''
Main runner entry point for Gooey.
'''

import wx
import wx.lib.inspection
from gooey.gui.lang import i18n

from gooey.gui import image_repository
from gooey.gui.containers.application import GooeyApplication
from gooey.util.functional import merge


def run(build_spec):
  app = build_app(build_spec)
  app.MainLoop()


def build_app(build_spec):
  app = wx.App(False)

  i18n.load(build_spec['language_dir'], build_spec['language'], build_spec['encoding'])
  imagesPaths = image_repository.loadImages(build_spec['image_dir'])
  gapp = GooeyApplication(merge(build_spec, imagesPaths))
  # wx.lib.inspection.InspectionTool().Show()
  gapp.Show()
  return app




