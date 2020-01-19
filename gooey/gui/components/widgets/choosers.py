from gooey.gui.components.widgets import core
from gooey.gui.components.widgets.bases import TextContainer, BaseChooser


__ALL__ = [
    'FileChooser',
    'FileSaver',
    'DirChooser',
    'MultiDirChooser',
    'DateChooser',
    'ColourChooser'
]

class FileChooser(BaseChooser):
    # todo: allow wildcard from argparse
    widget_class = core.FileChooser


class MultiFileChooser(BaseChooser):
    # todo: allow wildcard from argparse
    widget_class = core.MultiFileChooser


class FileSaver(BaseChooser):
    # todo: allow wildcard
    widget_class = core.FileSaver


class DirChooser(BaseChooser):
    # todo: allow wildcard
    widget_class = core.DirChooser


class MultiDirChooser(BaseChooser):
    # todo: allow wildcard
    widget_class = core.MultiDirChooser


class DateChooser(BaseChooser):
    # todo: allow wildcard
    widget_class = core.DateChooser


class ColourChooser(BaseChooser):
    widget_class = core.ColourChooser