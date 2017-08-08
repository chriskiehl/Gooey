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




