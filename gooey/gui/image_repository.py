'''
Collection of the image paths.

The module is meant to act as a singleton, hence the globals() abuse.

Image credit: kidcomic.net
'''
import os
from functools import partial
import warnings

from gooey.gui.util.freeze import getResourcePath
from gooey.util.functional import merge

filenames = {
    'programIcon': 'program_icon.png',
    'successIcon': 'success_icon.png',
    'runningIcon': 'running_icon.png',
    'configIcon': 'config_icon.png',
    'errorIcon': 'error_icon.png'
}

valid_ext = ('.png', '.jpg', '.gif')


def loadImages(targetDir):
    return {'images': merge(
        resolvePaths(getResourcePath('images'), filenames, valid_ext),
        resolvePaths(getImageDirectory(targetDir), filenames, valid_ext))
    }


def getImageDirectory(targetDir):
    return getResourcePath('images') \
           if targetDir == '::gooey/default' \
           else targetDir


def collectOverrides(targetDir, filenames):
    if targetDir == '::gooey/default':
        return {}

    pathto = partial(os.path.join, targetDir)
    if not os.path.isdir(targetDir):
        raise IOError('Unable to find the user supplied directory {}'.format(
            targetDir))

    return {varname: pathto(filename)
            for varname, filename in filenames.items()
            if os.path.exists(pathto(filename))}


def resolvePaths(dirname, filenames, valid_ext):

    # Find candidate file paths (allow different ext casing)
    valid_ext = {e.lower() for e in valid_ext}

    filePaths = {}
    for f in sorted(os.listdir(dirname)):
        name, ext = os.path.splitext(f)
        if ext.lower() not in valid_ext:
            continue

        if name in filePaths:
            warnings.warn('Multiple {} images found, using last found '
                          'extension ({})'.format(name, ext))
        filePaths[name] = os.path.join(dirname, f)

    # Build image dict
    return {key: filePaths[os.path.splitext(name)[0]]
            for key, name in filenames.items() if
            os.path.splitext(name)[0] in filePaths}

