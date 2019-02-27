from gooey.gui.lang.i18n import _

import wx

from gooey.gui.three_to_four import Constants


class BaseDialog(wx.Dialog):
  """
    Common base for CalendarDlg and TimeDlg.
  """
  def __init__(self, parent, pickerClass, pickerGetter, localizedPickerLabel):
    wx.Dialog.__init__(self, parent, title=localizedPickerLabel)

    self.SetBackgroundColour('#ffffff')

    self.ok_button = wx.Button(self, wx.ID_OK, label=_('ok'))
    self.picker = pickerClass(self, style=Constants.WX_DP_DROPDOWN)
    self.pickerGetter = pickerGetter

    vertical_container = wx.BoxSizer(wx.VERTICAL)
    vertical_container.AddSpacer(10)
    vertical_container.Add(self.picker, 0, wx.LEFT | wx.RIGHT | wx.ALIGN_CENTER, 15)

    vertical_container.AddSpacer(10)
    button_sizer = wx.BoxSizer(wx.HORIZONTAL)
    button_sizer.AddStretchSpacer(1)
    button_sizer.Add(self.ok_button, 0)

    vertical_container.Add(button_sizer, 0, wx.LEFT | wx.RIGHT | wx.ALIGN_CENTER, 15)
    vertical_container.AddSpacer(20)
    self.SetSizerAndFit(vertical_container)

    self.Bind(wx.EVT_BUTTON, self.onOkButton, self.ok_button)

  def onOkButton(self, event):
    self.EndModal(wx.ID_OK)
    event.Skip()

  def onCancelButton(self, event):
    try:
      return None
    except:
      self.Close()

  def GetPath(self):
    """
      Return the value chosen in the picker.
      The method is called GetPath() instead of getPath() to emulate the WX Pickers API.
      This allows the Chooser class to work same way with native WX dialogs or childs of BaseDialog.
    """

    return self.pickerGetter(self.picker)



