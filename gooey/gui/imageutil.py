'''
Utilities for loading, resizing and converting between PIL and WX image formats
'''

import six
from PIL import Image
import wx

from gooey.gui.three_to_four import imageFromBitmap, bitmapFromImage



def loadImage(img_path):
    return Image.open(img_path)


def resizeImage(im, targetHeight):
    im.thumbnail((six.MAXSIZE, targetHeight))
    return im


def wrapBitmap(im, parent):
    bitmapData = wx.Bitmap.FromBufferRGBA(im.size[0], im.size[1], im.convert('RGBA').tobytes())
    return wx.StaticBitmap(parent, bitmap=bitmapData)



if __name__ == '__main__':
    pass
