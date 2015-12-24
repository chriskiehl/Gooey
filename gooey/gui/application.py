'''
Main runner entry point for Gooey.
'''

import wx

from gooey.gui.lang import i18n
from gooey.gui.controller import Controller

from gooey.gui import image_repository



def run(build_spec):
  app = wx.App(False)

  i18n.load(build_spec['language_dir'], build_spec['language'])
  image_repository.patch_images(build_spec['image_dir'])
  controller = Controller(build_spec)
  controller.run()
  app.MainLoop()


