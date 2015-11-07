'''
Default Gooey icons.

Most icons provided by kidcomic.net
'''
import os
from gooey.gui.util.freeze import get_resource_path

image_dir = get_resource_path('images')

program_icon = os.path.join(image_dir, "program_icon.ico")
success_icon = os.path.join(image_dir, "success_checkmark.png")
running_icon = os.path.join(image_dir, "running_icon.png")
loading_icon = os.path.join(image_dir, "loading_icon.gif")
config_icon = os.path.join(image_dir, "config_icon.png")
error_icon = os.path.join(image_dir, "error_icon.png")










