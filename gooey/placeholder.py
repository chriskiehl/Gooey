import sys
import time

from PyQt5.QtCore import *
from PyQt5.QtCore import QTime
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QDialog, QTextBrowser, QLineEdit, \
    QVBoxLayout, QHBoxLayout, QGridLayout, QFileDialog
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QSpacerItem


'''
FileChooser       = build_subclass('FileChooser', widget_pack.FileChooserPayload)
MultiFileChooser  = build_subclass('MultiFileChooser', widget_pack.MultiFileSaverPayload)
DirChooser        = build_subclass('DirChooser', widget_pack.DirChooserPayload)
FileSaver         = build_subclass('FileSaver', widget_pack.FileSaverPayload)
DateChooser       = build_subclass('DateChooser', widget_pack.DateChooserPayload)
TextField         = build_subclass('TextField', widget_pack.TextInputPayload)
Textarea          = build_subclass('TextField', widget_pack.TextAreaPayload)
CommandField      = build_subclass('CommandField', widget_pack.TextInputPayload(no_quoting=True))
Dropdown          = build_subclass('Dropdown', widget_pack.DropdownPayload)
Counter           = build_subclass('Counter', widget_pack.CounterPayload)
MultiDirChooser   = build_subclass('MultiDirChooser', widget_pack.MultiDirChooserPayload)
'''



class Thing(object):

    def get_value(self):
        pass
    def set_value(self):
        pass



class FileChooser(object):

    def __init__(self):
        self.textfield = QLineEdit()
        self.button = QPushButton()
        layout = QHBoxLayout()
        layout.addWidget()



class Container(object):

    def __init__(self, label, help_text):
        row1 = QGridLayout()
        row1.setColumnMinimumWidth(0, 1)
        row1.setColumnMinimumWidth(1, 1)
        row1.addWidget(QLabel('<b>{}</b>'.format(label)), 0, 0)
        row1.addWidget(QLabel(help_text, wordWrap=True), 1, 0)
        # row1.addWidget(self.lineedit, 2, 0)



class Form(QDialog):

    def doSomething(self, e):
        print(e)

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.browser = QTextBrowser()
        self.lineedit = QLineEdit('Type an expression')
        self.lineedit.selectAll()
        self.lineedit.dropEvent.connect(self.doSomething)

        layout = QVBoxLayout()
        layout.addWidget(self.browser)


        row1 = QGridLayout()
        row1.setColumnMinimumWidth(0, 1)
        row1.setColumnMinimumWidth(1, 1)
        row1.addWidget(QLabel('<b>Filename is</b>'), 0,0)
        row1.addWidget(QLabel('hello I am a really long ttle and I have lots of words will I wrap my text? Find out next!!!', wordWrap=True), 1,0)
        row1.addWidget(self.lineedit, 2,0)

        btn = QPushButton('Open')
        btn.clicked.connect(self.showDialog)

        row1.addWidget(QLabel('<b>Shorter</b>'), 0, 1)
        # _layout2.addWidget(QSpacerItem())
        row1.addWidget(btn, 2, 1)
        row1.setColumnStretch(0, 1)
        row1.setColumnStretch(1, 1)
        print(row1.columnStretch(0))
        print(row1.columnStretch(1))

        layout.addLayout(row1)
        self.setLayout(layout)
        self.lineedit.setFocus()
        self.lineedit.returnPressed.connect(self.updateUi)
        self.setWindowTitle('Calculate')

    def updateUi(self):
        try:
            text = self.lineedit.text()
            self.browser.append("%s = <b>%s</b>" % (text, eval(text)))
        except:
            self.browser.append(
                "<font color=red>%s is invalid!</font>" % text
            )

    def showDialog(self):
        x = QFileDialog.getExistingDirectory(self, 'Open file')
        print(x)


app = QApplication(sys.argv)
form = Form()
form.show()
app.exec_()
