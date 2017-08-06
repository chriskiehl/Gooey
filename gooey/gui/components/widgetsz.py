# import json
# import sys
# from uuid import uuid4
#
# from PyQt5.QtWidgets import QFileDialog, QCalendarWidget, QDialogButtonBox, \
#     QComboBox, QCheckBox
#
# from PyQt5 import QtGui
#
# from PyQt5.QtCore import *
# from PyQt5.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout
# from PyQt5.QtWidgets import QFrame, QDialog
# from PyQt5.QtWidgets import QLabel
# from PyQt5.QtWidgets import QLineEdit, QTextEdit, QPlainTextEdit
# from PyQt5.QtWidgets import QPushButton
# from PyQt5.QtWidgets import QScrollArea
# from PyQt5.QtWidgets import QWidget, QMainWindow
#
# from copy import deepcopy
# from functools import reduce
# from gooey.gui.date_dialog import DateDialog
# from pydux import create_store, combine_reducers
#
# from rx.subjects import Subject
#
# class BaseWidget(QWidget):
#     widget_class = None
#
#     def arrange(self, label, text):
#         raise NotImplementedError
#
#     def getWidget(self, ):
#         return self.widget_class(self)
#
#     def connectSignal(self):
#         raise NotImplementedError
#
#     def getSublayout(self, *args, **kwargs):
#         raise NotImplementedError
#
#     def setValue(self, value):
#         raise NotImplementedError
#
#     def receiveChange(self, *args, **kwargs):
#         raise NotImplementedError
#
#     def dispatchChange(self, value, **kwargs):
#         raise NotImplementedError
#
#
# class TextContainer(BaseWidget):
#     widget_class = None
#
#     def __init__(self, parent, widgetInfo, *args, **kwargs):
#         super(TextContainer, self).__init__(parent, *args, **kwargs)
#
#         self._id = widgetInfo['id']
#         self.label = QLabel('<b>{}</b>'.format(widgetInfo['data']['display_name']))
#         self.help_text = QLabel(widgetInfo['data']['help'])
#         self.widget = self.getWidget()
#         self.layout = self.arrange(self.label, self.help_text)
#         self.value = Subject()
#         self.connectSignal()
#
#     def arrange(self, label, text):
#         layout = QVBoxLayout()
#         layout.addWidget(label, alignment=Qt.AlignTop)
#         if text:
#             layout.addWidget(text)
#         else:
#             layout.addStretch(1)
#         layout.addLayout(self.getSublayout())
#         return layout
#
#     def getWidget(self,):
#         return self.widget_class(self)
#
#     def connectSignal(self):
#         self.widget.textChanged.connect(self.dispatchChange)
#
#     def getSublayout(self, *args, **kwargs):
#         raise NotImplementedError
#
#     def setValue(self, value):
#         raise NotImplementedError
#
#     def receiveChange(self, *args, **kwargs):
#         raise NotImplementedError
#
#     def dispatchChange(self, value, **kwargs):
#         raise NotImplementedError
#
#
# class TextField(TextContainer):
#     widget_class = QLineEdit
#
#     def getSublayout(self, *args, **kwargs):
#         layout = QHBoxLayout()
#         layout.addWidget(self.widget)
#         return layout
#
#     def setValue(self, value):
#         self.widget.setText(value)
#
#     def connectSignal(self):
#         self.widget.textChanged.connect(self.dispatchChange)
#
#     def dispatchChange(self, value, **kwargs):
#         self.value.on_next({'value': value, 'id': self._id})
#
#
# class PasswordField(TextField):
#     def __init__(self, *args, **kwargs):
#         super(PasswordField, self).__init__(*args, **kwargs)
#         self.widget.setEchoMode(QLineEdit.Password)
#
#
# class Textarea(TextField):
#     widget_class = QTextEdit
#
#     def receiveChange(self):
#         currentState = self._store.get_state()['widgets'][self._id]['value']
#         print('received_change! current state = ', currentState)
#         if self.widget.toPlainText() != currentState:
#             self.widget.document().setPlainText(currentState)
#
#     def dispatchChange(self, *args, **kwargs):
#         print('dispatching change for component with ID:', self._id)
#         self.widget.on_next({
#             'type': 'UPDATE_WIDGET',
#             'value':  self.widget.toPlainText(),
#             'id': self._id
#         })
#
#
# class Chooser(TextField):
#     widget_class = QLineEdit
#     launchDialog = None
#
#     def getSublayout(self, *args, **kwargs):
#         self.button = QPushButton('Browse')
#         self.button.clicked.connect(self.spawnDialog)
#
#         layout = QHBoxLayout()
#         layout.addWidget(self.widget, stretch=1)
#         layout.addWidget(self.button)
#         return layout
#
#     def spawnDialog(self, *args, **kwargs):
#         if not callable(self.launchDialog):
#             raise AssertionError(
#                 'Chooser subclasses must provide QFileDialog callable '
#                 'to launchDialog property (.e.g '
#                 '`launchDialog = QFileDialog.getOpenFileName`'
#             )
#         result = self.launchDialog(parent=self)
#         if result:
#             self.setValue(self.processResult(result))
#
#     def processResult(self, result):
#         return result[0]
#
#
# # TODO: unify all of the return types Qt throws out
# # TODO: of the various Dialogs
# class DateChooser(Chooser):
#     launchDialog = DateDialog.getUserSelectedDate
#
#
# class FileSaver(Chooser):
#     launchDialog = QFileDialog.getSaveFileName
#
#
# class FileChooser(Chooser):
#     launchDialog = QFileDialog.getOpenFileName
#
#
# class MultiFileChooser(Chooser):
#     launchDialog = QFileDialog.getOpenFileNames
#
#     def processResult(self, result):
#         return ', '.join(result[0])
#
#
# class DirectoryChooser(Chooser):
#     launchDialog = QFileDialog.getExistingDirectory
#
#     def processResult(self, result):
#         return result
#
#
# class Dropdown(TextContainer):
#     widget_class = QComboBox
#
#     def __init__(self, parent, widgetInfo, *args, **kwargs):
#         super(Dropdown, self).__init__(parent, widgetInfo, *args, **kwargs)
#
#         # initialize dropdown values
#         for choice in widgetInfo['data']['choices']:
#             self.widget.addItem(choice)
#
#         if widgetInfo['data']['default']:
#             self.setValue(widgetInfo['data']['default'])
#
#     def getSublayout(self, *args, **kwargs):
#         layout = QHBoxLayout()
#         layout.addWidget(self.widget)
#         return layout
#
#     def connectSignal(self):
#         self.widget.currentIndexChanged.connect(self.dispatchChange)
#
#     def setValue(self, value):
#         self.widget.setCurrentIndex(value)
#
#     def dispatchChange(self, value, **kwargs):
#         self.value.on_next({'value': value, 'id': self._id})
#         # QTimer.singleShot(0, lambda: self._store.dispatch({})
#
#
# class Counter(Dropdown):
#     pass
#
#
# class CheckBox(BaseWidget):
#
#     def __init__(self, parent, widgetInfo, *args, **kwargs):
#         super(CheckBox, self).__init__(parent, *args, **kwargs)
#         self._id = widgetInfo['id']
#         self.label = QLabel('<b>{}</b>'.format(widgetInfo['data']['display_name']))
#         self.widget = QCheckBox(widgetInfo['data']['help'] or '')
#
#         self.layout = self.arrange()
#         self.value = Subject()
#         self.connectSignal()
#
#         if widgetInfo['data']['default']:
#             self.setValue(widgetInfo['data']['default'])
#
#     def arrange(self):
#         layout = QVBoxLayout()
#         layout.addWidget(self.label, alignment=Qt.AlignTop)
#         layout.addWidget(self.widget)
#         return layout
#
#     def connectSignal(self):
#         self.widget.stateChanged.connect(self.dispatchChange)
#
#     def setValue(self, value):
#         self.widget.setChecked(value)
#
#     def dispatchChange(self, value, **kwargs):
#         self.value.on_next({
#             'value': self.widget.checkState,
#             'id': self._id
#         })
