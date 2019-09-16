'''
Utils for retrieving resources when when in a frozen state.

MEIPASS explanation:
https://pythonhosted.org/PyInstaller/#run-time-operation
'''
import os
import sys


def is_frozen():
    return getattr(sys, 'frozen', False)


def getResourcePath(*args):
    if is_frozen():
        # MEIPASS explanation:
        # https://pythonhosted.org/PyInstaller/#run-time-operation
        basedir = getattr(sys, '_MEIPASS', None)
        if not basedir:
            basedir = os.path.dirname(sys.executable)
        resource_dir = os.path.join(basedir, 'gooey')
        if not os.path.isdir(resource_dir):
            raise IOError(
                (
                "Cannot locate Gooey resources. It seems that the program was frozen, "
                "but resource files were not copied into directory of the executable "
                "file. Please copy `languages` and `images` folders from gooey module "
                "directory into `{}{}` directory. Using PyInstaller, a.datas in .spec "
                "file must be specified.".format(resource_dir, os.sep)))
    else:
        resource_dir = os.path.normpath(
            os.path.join(os.path.dirname(__file__), '..', '..'))
    return os.path.join(resource_dir, *args)


def localResourcePath(path):
    """
    A packaging aware util for getting the path to the local working directory.
    When non-packaged, this is os.getcwd(), when packaged, it will be the local
    (dynamic) directory where PyInstaller decompresses content.
    """
    if is_frozen():
        basedir = getattr(sys, '_MEIPASS', None)
        return os.path.join(basedir or sys.executable, path)
    else:
        return os.path.join(os.getcwd(), path)
