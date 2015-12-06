'''
Collection of the image paths.

The module is meant to act as a singleton, hence the globals() abuse.

Image credit: kidcomic.net
'''
from functools import partial
import os
from gooey.gui.util.freeze import get_resource_path

_image_details = (
  ('program_icon', 'program_icon.ico'),
  ('success_icon', 'success_icon.png'),
  ('running_icon', 'running_icon.png'),
  ('loading_icon', 'loading_icon.gif'),
  ('config_icon', 'config_icon.png'),
  ('error_icon', 'error_icon.png')
)

def init(image_dir):
  ''' initalize the images from the default directory path '''
  defaults = {variable_name: os.path.join(image_dir, filename)
              for variable_name, filename in _image_details}
  globals().update(defaults)

def patch_images(new_image_dir):
  '''
  Loads custom images from the user supplied directory
  '''
  pathto = partial(os.path.join, new_image_dir)

  if new_image_dir != 'default':
    if not os.path.isdir(new_image_dir):
      raise IOError('Unable to find the user supplied directory {}'.format(new_image_dir))

    new_images = ((varname, pathto(filename))
                           for varname, filename in _image_details
                           if os.path.exists(pathto(filename)))
    # push the changes into module scope
    globals().update(new_images)


default_dir = get_resource_path('images')
init(default_dir)














