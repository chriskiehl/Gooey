import wx
import os

from gooey.gui.components.widgets.core.text_input import TextInput
from gooey.gui.components.widgets.dialogs.calender_dialog import CalendarDlg
from gooey.gui.lang.i18n import _
from gooey.util.functional import merge


class Chooser(wx.Panel):
    """
    Base 'Chooser' type.

    Launches a Dialog box that allows the user to pick files, directories,
    dates, etc.. and places the result into a TextInput in the UI
    """

    def __init__(self, parent, *args, **kwargs):
        super(Chooser, self).__init__(parent)
        buttonLabel = kwargs.pop('label', _('browse'))
        self.widget = TextInput(self, *args, **kwargs)
        self.button = wx.Button(self, label=buttonLabel)
        self.button.Bind(wx.EVT_BUTTON, self.spawnDialog)
        self.layout()


    def layout(self):
        layout = wx.BoxSizer(wx.HORIZONTAL)
        layout.Add(self.widget, 1, wx.EXPAND | wx.TOP, 2)
        layout.Add(self.button, 0, wx.LEFT, 10)

        v = wx.BoxSizer(wx.VERTICAL)
        v.Add(layout, 1, wx.EXPAND, wx.TOP, 1)
        self.SetSizer(v)


    def spawnDialog(self, event):
        fd = self.getDialog()
        if fd.ShowModal() == wx.ID_CANCEL:
            return
        self.processResult(self.getResult(fd))


    def getDialog(self):
        return wx.FileDialog(self, _('open_file'))

    def getResult(self, dialog):
        return dialog.GetPath()


    def processResult(self, result):
        self.setValue(result)


    def setValue(self, value):
        self.widget.setValue(value)

    def getValue(self):
        return self.widget.getValue()



class FileChooser(Chooser):
    """ Retrieve an existing file from the system """
    def getDialog(self):
        return wx.FileDialog(self, style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)


class MultiFileChooser(Chooser):
    """ Retrieve an multiple files from the system """
    def getDialog(self):
        return wx.FileDialog(self, "Open Files" ,style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE)
    def getResult(self, dialog):
        return os.pathsep.join(dialog.GetPaths()) 


class FileSaver(Chooser):
    """ Specify the path to save a new file """
    def getDialog(self):
        return wx.FileDialog(
            self,
            style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT,
            defaultFile=_("enter_filename"),
            message=_('choose_file')
        )


class DirChooser(Chooser):
    """ Retrieve a path to the supplied directory """
    def getDialog(self):
        return wx.DirDialog(self, message=_('choose_folder'))


class DateChooser(Chooser):
    """ Launches a date picker which returns and ISO Date """
    def __init__(self, *args, **kwargs):
        defaults = {'label': _('choose_date')}
        super(DateChooser, self).__init__(*args, **merge(kwargs, defaults))


    def getDialog(self):
        return CalendarDlg(self)





