'''
Utilities for loading, resizing and converting between PIL and WX image formats
'''

import six
from PIL import Image, ImageSequence
import wx

from gooey.gui.three_to_four import bitmapFromBufferRGBA



def loadImage(img_path):
    return Image.open(img_path)


def resizeImage(im, targetHeight):
    im.thumbnail((six.MAXSIZE, targetHeight))
    return im


def resizeGif(imgPath, tmpPath, targetHeight):
    """https://gist.github.com/skywodd/8b68bd9c7af048afcedcea3fb1807966"""

    # Read image and get target width to maintain aspect ratio (only downsize)
    im = Image.open(imgPath)
    if im.size[1] < targetHeight:
        targetWidth, targetHeight = im.size
    else:
        targetWidth = int(im.size[0] * (targetHeight / im.size[1]))

    # Frame generator
    frames = (f.copy().resize((targetWidth, targetHeight), Image.ANTIALIAS) for
              f in ImageSequence.Iterator(im))

    # Save output
    gif = next(frames)
    gif.info = im.info
    gif.save(tmpPath, format=im.format, save_all=True,
             append_images=list(frames), quality=95)

    return tmpPath


def wrapBitmap(im, parent):
    try:
        rgba = im.convert('RGBA').tobytes()
    except AttributeError:
        rgba = im.convert('RGBA').tostring()

    bitmapData = bitmapFromBufferRGBA(im, rgba)
    return wx.StaticBitmap(parent, bitmap=bitmapData)


if __name__ == '__main__':
    pass
