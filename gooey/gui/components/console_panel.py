from PyQt5.QtWidgets import QVBoxLayout, QTextEdit
from PyQt5.QtWidgets import QWidget


class ConsolePanel(QWidget):

    def __init__(self, parent, *args, **kwargs):
        super(ConsolePanel, self).__init__(parent, *args, **kwargs)
        self.widget = QTextEdit()
        self.widget.setReadOnly(True)
        # doc = self.widget.document()
        # font = doc.defaultFont()
        # font.setFamily('Courier New')
        # doc.setDefaultFont(font)

        self.layoutComponent()

    def layoutComponent(self):
        layout = QVBoxLayout()
        layout.addWidget(self.widget, stretch=1)
        self.setLayout(layout)


    def writeLine(self, line):
        self.widget.append(line)
        c = self.widget.textCursor()
        c.movePosition(c.End)
        self.widget.setTextCursor(c)
