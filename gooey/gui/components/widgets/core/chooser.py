import wx
import wx.lib.agw.multidirdialog as MDD
import os
import re

from gooey.gui.components.widgets.core.text_input import TextInput
from gooey.gui.components.widgets.dialogs.calender_dialog import CalendarDlg
from gooey.gui.components.widgets.dialogs.time_dialog import TimeDlg
from gooey.gui.lang.i18n import _
from gooey.util.functional import merge
from gooey.gui.util.filedrop import FileDrop


class Chooser(wx.Panel):
    """
    TODO: Tests!
    TODO: Document GooeyOptions!
    Base 'Chooser' type.

    Launches a Dialog box that allows the user to pick files, directories,
    dates, etc.. and places the result into a TextInput in the UI

    TODO: oh, young me. DRY != Good Abstraction
    TODO: this is another weird inheritance hierarchy that's hard
          to follow. Why do subclasses reach into, not their parent
          class, but their _physical_ UI parent to grab the Gooey Options?
          All this could be simplified to make the data flow
          more apparent.
    """
    _gooey_options = {
        'pathsep': str
    }
    def __init__(self, parent, *args, **kwargs):
        super(Chooser, self).__init__(parent)
        self.options = parent._options
        buttonLabel = kwargs.pop('label', _('browse'))
        self.widget = TextInput(self, *args, **kwargs)
        self.button = wx.Button(self, label=buttonLabel)
        self.button.Bind(wx.EVT_BUTTON, self.spawnDialog)
        self.dropTarget = FileDrop(self.widget, self.dropHandler)
        self.widget.SetDropTarget(self.dropTarget)
        self.layout()

    def dropHandler(self, x, y, filenames):
        sep = self.options.get('pathsep', os.pathsep)
        self.widget.setValue(sep.join(filenames))
        return True

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

    def SetHint(self, value):
        self.widget.SetHint(value)

    def getValue(self):
        return self.widget.getValue()


class FileChooser(Chooser):
    """ Retrieve an existing file from the system """
    def getDialog(self):
        options = self.Parent._options
        return wx.FileDialog(self, message=options.get('message', _('open_file')),
                             style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST,
                             defaultFile=options.get('default_file', _("enter_filename")),
                             defaultDir=options.get('default_dir', _('')),
                             wildcard=options.get('wildcard', wx.FileSelectorDefaultWildcardStr))


class MultiFileChooser(Chooser):
    """ Retrieve an multiple files from the system """
    def getDialog(self):
        options = self.Parent._options
        return wx.FileDialog(self, message=options.get('message', _('open_files')),
                             style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE,
                             defaultFile=options.get('default_file', _("enter_filename")),
                             defaultDir=options.get('default_dir', _('')),
                             wildcard=options.get('wildcard', wx.FileSelectorDefaultWildcardStr))

    def getResult(self, dialog):
        return os.pathsep.join(dialog.GetPaths())


class FileSaver(Chooser):
    """ Specify the path to save a new file """
    def getDialog(self):
        options = self.Parent._options
        return wx.FileDialog(
            self,
            style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT,
            defaultFile=options.get('default_file', _("enter_filename")),
            defaultDir=options.get('default_dir', _('')),
            message=options.get('message', _('choose_file')),
            wildcard=options.get('wildcard', wx.FileSelectorDefaultWildcardStr)
        )


class DirChooser(Chooser):
    """ Retrieve a path to the supplied directory """
    def getDialog(self):
        options = self.Parent._options
        return wx.DirDialog(self, message=options.get('message', _('choose_folder')),
                            defaultPath=options.get('default_path', os.getcwd()))

class MultiDirChooser(Chooser):
    """ Retrieve multiple directories from the system """
    def getDialog(self):
        options = self.Parent._options
        return MDD.MultiDirDialog(self,
                                  message=options.get('message', _('choose_folders')),
                                  title=_('choose_folders_title'),
                                  defaultPath=options.get('default_path', os.getcwd()),
                                  agwStyle=MDD.DD_MULTIPLE | MDD.DD_DIR_MUST_EXIST)
    def getResult(self, dialog):
        paths = dialog.GetPaths()
        # Remove volume labels from Windows paths
        if 'nt' == os.name:
            for i, path in enumerate(paths):
                if path:
                    parts = path.split(os.sep)
                    vol = parts[0]
                    drives = re.match(r'.*\((?P<drive>\w:)\)', vol)
                    paths[i] = os.sep.join([drives.group('drive')] + parts[1:])

        return os.pathsep.join(paths)


class DateChooser(Chooser):
    """ Launches a date picker which returns an ISO Date """
    def __init__(self, *args, **kwargs):
        defaults = {'label': _('choose_date')}
        super(DateChooser, self).__init__(*args, **merge(kwargs, defaults))

    def getDialog(self):
        return CalendarDlg(self)


class TimeChooser(Chooser):
    """ Launches a time picker which returns and ISO Time """
    def __init__(self, *args, **kwargs):
        defaults = {'label': _('choose_time')}
        super(TimeChooser, self).__init__(*args, **merge(kwargs, defaults))

    def getDialog(self):
        return TimeDlg(self)


class ColourChooser(Chooser):
    """ Launches a color picker which returns a hex color code"""
    def __init__(self, *args, **kwargs):
        defaults = {'label': _('choose_colour'),
                    'style': wx.TE_RICH}
        super(ColourChooser, self).__init__(*args, **merge(kwargs, defaults))

    def setValue(self, value):
        colour = wx.Colour(value)
        self.widget.widget.SetForegroundColour(colour)
        self.widget.widget.SetBackgroundColour(colour)
        self.widget.setValue(value)

    def getResult(self, dialog):
        colour = dialog.GetColourData().GetColour()

        # Set text box back/foreground to selected colour
        self.widget.widget.SetForegroundColour(colour)
        self.widget.widget.SetBackgroundColour(colour)

        return colour.GetAsString(wx.C2S_HTML_SYNTAX)

    def getDialog(self):
        return wx.ColourDialog(self)
