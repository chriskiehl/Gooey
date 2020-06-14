"""
All of the dialogs used throughout Gooey
"""
from collections import namedtuple

import wx

from gooey.gui.lang.i18n import _


# These don't seem to be specified anywhere in WX for some reason
DialogConstants = namedtuple('DialogConstants', 'YES NO')(5103, 5104)


def showDialog(title, content, style):
    dlg = wx.MessageDialog(None, content, title, style)
    dlg.SetYesNoLabels(_('dialog_button_yes'), _('dialog_button_no'))
    dlg.SetOKLabel(_('dialog_button_ok'))
    result = dlg.ShowModal()
    dlg.Destroy()
    return result


def missingArgsDialog():
    showDialog(_('error_title'), _('error_required_fields'), wx.ICON_ERROR)


def validationFailure():
    showDialog(_('error_title'), _('validation_failed'), wx.ICON_WARNING)


def showSuccess():
    showDialog(_('execution_finished'), _('success_message'), wx.ICON_INFORMATION)


def showFailure():
    showDialog(_('execution_finished'), _('uh_oh'), wx.ICON_ERROR)


def confirmExit():
    result = showDialog(_('sure_you_want_to_exit'), _('close_program'), wx.YES_NO | wx.ICON_INFORMATION)
    return result == DialogConstants.YES


def confirmForceStop():
    result = showDialog(_('stop_task'), _('sure_you_want_to_stop'), wx.YES_NO | wx.ICON_WARNING)
    return result == DialogConstants.YES

