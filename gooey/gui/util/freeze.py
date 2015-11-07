import sys
import os


def is_frozen():
  return getattr(sys, 'frozen', False)


def get_resource_path(*args):
  if is_frozen():
    # MEIPASS explanation:
    # https://pythonhosted.org/PyInstaller/#run-time-operation
    resource_dir = os.path.join(sys._MEIPASS, 'gooey')
    if not os.path.isdir(resource_dir):
      raise IOError(("cannot locate Gooey resources. It seems that the program "
                     "was frozen, but resource files were not copied to "
                     "directory of the executable file. Please copy "
                     "`languages` and `images` folders from gooey module "
                     "directory into `{}{}` directory.".format(resource_dir, os.sep)))
  else:
    resource_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..'))
  return os.path.join(resource_dir, *args)
