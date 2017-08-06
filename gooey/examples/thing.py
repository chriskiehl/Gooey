import sys
import time
import json

from PyQt5.QtCore import *
from PyQt5.QtCore import QTime
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QDialog, QTextBrowser, QLineEdit, \
    QVBoxLayout, QHBoxLayout, QGridLayout, QFileDialog, QDialogButtonBox, QFrame, \
    QCheckBox, QComboBox, QDateEdit, QRadioButton, QWidget
from PyQt5.QtWidgets import QGroupBox
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



class Generic(QWidget):

    def __init__(self, *args, **kwargs):
        self._store = kwargs.pop('store')
        self._store.subscribe(self.handlechange)
        super(Generic, self).__init__(*args, **kwargs)

    def handlechange(self):
        pass


class Container(object):

    def __init__(self, label, help_text):
        self.label = QLabel('<b>{}</b>'.format(label))
        self.help_text = QLabel(help_text, wordWrap=True, alignment=Qt.AlignTop)

        self.layout = self.arrange(self.label, self.help_text)

    def arrange(self, label, text):
        layout = QVBoxLayout()
        layout.addWidget(label, alignment=Qt.AlignTop)
        if text:
            layout.addWidget(text)
        else:
            layout.addStretch(1)
        layout.addLayout(self.get_sublayout())
        return layout

    def get_sublayout(self, *args, **kwargs):
        raise NotImplemented


class TextField(Container):

    def get_sublayout(self, *args, **kwargs):
        self.widget = QLineEdit(*args, **kwargs)
        layout = QHBoxLayout()
        layout.addWidget(self.widget)
        return layout


class FileChooser(Container):

    def get_sublayout(self, *args, **kwargs):
        self.textfield = QLineEdit()
        self.button = QPushButton('Browse')

        layout = QHBoxLayout()
        layout.addWidget(self.textfield)
        layout.addWidget(self.button)
        return layout


class Checkbox(Container):

    def arrange(self, label, text):
        internal_layout = QHBoxLayout()
        internal_layout.addLayout(self.get_sublayout())
        internal_layout.addSpacing(10)
        internal_layout.addWidget(text)

        parent_layout = QVBoxLayout()
        parent_layout.addWidget(label)

        parent_layout.addLayout(internal_layout)
        return parent_layout

    def get_sublayout(self, *args, **kwargs):
        self.checkbox = QCheckBox()
        layout = QHBoxLayout()
        layout.addWidget(self.checkbox)
        return layout


class Dropdown(Container):

    def get_sublayout(self, *args, **kwargs):
        self.widget = QComboBox()
        self.widget.addItems(map(str, [1,2,3]))
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.widget)
        return self.layout


class DateChooser(Container):
    def get_sublayout(self, *args, **kwargs):
        self.widget = QDateEdit()
        self.widget.setCalendarPopup(True)
        layout = QVBoxLayout()
        layout.addWidget(self.widget)
        return layout


class RadioGroup(Container):

    def arrange(self, label, text):
        box = QGroupBox("uhhhh umm hmm")
        box.setFlat(True)
        a = QRadioButton('one')
        b = QRadioButton('two')
        internal_layout = QVBoxLayout()
        internal_layout.addWidget(a)
        internal_layout.addWidget(b)
        box.setLayout(internal_layout)
        return box

    def get_sublayout(self, *args, **kwargs):
        self.checkbox = QCheckBox()
        layout = QHBoxLayout()
        layout.addWidget(self.checkbox)
        return layout


tmp = {
    'RadioGroup': RadioGroup,
    'DateChooser': DateChooser,
    'Dropdown': Dropdown,
    'Checkbox': Checkbox,
    'FileChooser':FileChooser,
    'TextField':TextField
}


class Form(QDialog):

    def doSomething(self, e):
        print(e)

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.browser = QTextBrowser()
        self.lineedit = QLineEdit('Type an expression')
        self.lineedit.selectAll()

        with open('gooey_config.json', 'rb') as f:
            data = json.loads(f.read().decode('utf-8'))

        # widgets = []
        # for i, j in data['widgets'].items():
        #     for k in j['contents']:
        #         if k['type'] in tmp:
        #             widgets.append(tmp[k[type]]())

        layout = QVBoxLayout()
        layout.addWidget(self.browser)


        row1 = QHBoxLayout()
        row1.addStretch(1)
        row1.addItem(
            TextField(
                '<b>Filename is</b>',
                'hello I am a really long ttle and I have lots of words will I wrap my text? Find out next!!!',
            ).layout,
        )

        row1.addItem(
            FileChooser(
                '<b>Something</b>',
                'hello I am a really long ttle and I have lots of words will I wrap my text? Find out next!!!',
            ).layout,
        )

        row1.addItem(
            Checkbox(
                '<b>Recurse (-r)</b>',
                'recurse into subdirectories',
            ).layout,
        )

        row1.addItem(
            Dropdown(
                '<b>Verbosity Level (-v)</b>',
                'Set the verbosity of the output',
            ).layout,
        )

        row1.addItem(
            DateChooser(
                '<b>Start Date (-s)</b>',
                'Cron start date',
            ).layout,
        )

        row1.addWidget(
            RadioGroup(
                'foo',
                'bar'
            ).layout
        )


        layout.addLayout(row1)
        self.setLayout(layout)
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
