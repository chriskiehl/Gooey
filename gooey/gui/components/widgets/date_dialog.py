from PyQt5.QtCore import *
from PyQt5.QtWidgets import QCalendarWidget
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QVBoxLayout


class DateDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(DateDialog, self).__init__(*args, **kwargs)
        layout = QVBoxLayout(self)
        calendar = QCalendarWidget(self)
        calendar.setGridVisible(True)
        calendar.clicked.connect(self.selected_date)
        layout.addWidget(calendar)
        self.setLayout(layout)

    def selected_date(self, date):
        self.result = date.toString(Qt.ISODate)
        self.accept()

    @staticmethod
    def getUserSelectedDate(*args, **kwargs):
        dialog = DateDialog()
        if dialog.exec():
            # The result is wrapped in a tuple to match
            # the return style of the QFileDialog variants
            # it is mimicking
            return (dialog.result, )

