'''
Created on Jan 23, 2014

@author: Chris
'''
import wx


def ShowError(msg):
  wx.MessageDialog(
    None,
    msg,
    'Argument Error',
    wx.ICON_ERROR)


if __name__ == '__main__':
  pass