from PyQt5.QtWidgets import QLabel, QListWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget
from rx.subjects.subject import Subject


class Sidebar(QWidget):
    def __init__(self, parent, contents, *args, **kwargs):
        super(Sidebar, self).__init__(parent, *args, **kwargs)
        self.value = Subject()
        self.widget = self.buildListWidget(contents)
        self.widget.currentRowChanged.connect(self.dispatchChanges)
        self.layoutComponent()

    def buildListWidget(self, contents):
        widget = QListWidget(self)
        for item in contents:
            widget.addItem(item)
        widget.setCurrentRow(0)
        return widget

    def layoutComponent(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel('<h3>Actions</h3>'))
        layout.addWidget(self.widget, stretch=1)
        self.setLayout(layout)

    def dispatchChanges(self, currentRow):
        self.value.on_next({
            'type': 'SELECTION_CHANGE',
            'value': currentRow,
            'group': self.widget.currentItem().text()
        })
