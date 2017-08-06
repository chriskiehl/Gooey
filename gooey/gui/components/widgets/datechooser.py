from gooey.gui.components.widgets.chooser import Chooser
from gooey.gui.components.widgets.date_dialog import DateDialog


class DateChooser(Chooser):
    '''
    Launches a modal containing a Calendar with selectable dates
    '''
    launchDialog = DateDialog.getUserSelectedDate

