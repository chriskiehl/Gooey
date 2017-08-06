from PyQt5.QtWidgets import QFrame, QVBoxLayout, QWidget


def line(parent, direction):
    '''
    Generates a vertical or horizontal line widget

    :param direction: QFrame.HLine | QFrame.VLine
    '''
    frame = QFrame(parent)
    frame.setFrameShape(direction)
    frame.setFrameShadow(QFrame.Sunken)
    # frame.setLineWidth(2)
    return frame


def withMaxSize(parent, widget, maxSize):
    '''
    Wraps the target widget in another QWidget so that we
    can limit its max size independent of the host layout
    '''
    wrapped = QWidget(parent)
    wrapped.setMaximumWidth(maxSize)
    layout = QVBoxLayout()
    layout.addWidget(widget)
    wrapped.setLayout(layout)
    return wrapped
