'''
Collection of the image paths.

The module is meant to act as a singleton, hence the globals() abuse.

Image credit: kidcomic.net
'''
import os
from functools import partial

from gooey.gui.util.freeze import getResourcePath
from gooey.util.functional import merge

filenames = {
    'programIcon': 'program_icon.png',
    'successIcon': 'success_icon.png',
    'runningIcon': 'running_icon.png',
    'configIcon': 'config_icon.png',
    'errorIcon': 'error_icon.png'
}


def loadImages(targetDir):
    defaultImages = resolvePaths(getResourcePath('images'), filenames)
    return {'images': merge(defaultImages, collectOverrides(targetDir, filenames))}


def getImageDirectory(targetDir):
    return getResourcePath('images') \
           if targetDir == 'default' \
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


def resolvePaths(dirname, filenames):
    return {key:  os.path.join(dirname, filename)
            for key, filename in filenames.items()}


