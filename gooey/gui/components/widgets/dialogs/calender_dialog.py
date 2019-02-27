

from .base_dialog import BaseDialog
from gooey.gui.three_to_four import Classes
from gooey.gui.lang.i18n import _


class CalendarDlg(BaseDialog):
    def __init__(self, parent):
        super(CalendarDlg, self).__init__(parent, 
            pickerClass=Classes.DatePickerCtrl,
            pickerGetter=lambda datepicker: datepicker.GetValue().FormatISODate(),
            localizedPickerLabel=_('select_date'))