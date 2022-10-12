from gooey.gui.three_to_four import Classes
from gooey.gui.lang.i18n import _
from .base_dialog import BaseDialog


class TimeDlg(BaseDialog):
    def __init__(self, parent):
        super().__init__(parent,
			pickerClass=Classes.TimePickerCtrl,
			pickerGetter=lambda datepicker: datepicker.GetValue().FormatISOTime(),
			localizedPickerLabel=_('select_time'))
