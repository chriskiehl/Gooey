'''
Util for supporting WxPython 3 & 4
'''

import wx
try:
    import wx.adv
except ImportError:
    pass

isLatestVersion = wx.version().startswith('4')


class Constants:
    if isLatestVersion:
        WX_FONTSTYLE_NORMAL = wx.FONTSTYLE_NORMAL
        WX_DP_DROPDOWN = wx.adv.DP_DROPDOWN
    else:
        WX_FONTSTYLE_NORMAL = wx.FONTWEIGHT_NORMAL
        WX_DP_DROPDOWN = wx.DP_DROPDOWN


class Classes:
    if isLatestVersion:
        DatePickerCtrl = wx.adv.DatePickerCtrl
    else:
        DatePickerCtrl = wx.DatePickerCtrl

    if isLatestVersion:
        TimePickerCtrl = wx.adv.TimePickerCtrl
    else:
        TimePickerCtrl = wx.TimePickerCtrl




def imageFromBitmap(bitmap):
    if isLatestVersion:
        return bitmap.ConvertToImage()
    else:
        return wx.ImageFromBitmap(bitmap)


def bitmapFromImage(image):
    if isLatestVersion:
        return wx.Bitmap(image)
    else:
        return wx.BitmapFromImage(image)


def bitmapFromBufferRGBA(im, rgba):
    if isLatestVersion:
        return wx.Bitmap.FromBufferRGBA(im.size[0], im.size[1], rgba)
    else:
        return wx.BitmapFromBufferRGBA(im.size[0], im.size[1], rgba)

def AboutDialog():
    if isLatestVersion:
        return wx.adv.AboutDialogInfo()
    else:
        return wx.AboutDialogInfo()


def AboutBox(aboutDialog):
    return (wx.adv.AboutBox(aboutDialog)
            if isLatestVersion
            else wx.AboutBox(aboutDialog))

