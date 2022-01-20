"""
Parser containing all Gooey widgets.
"""

from gooey import GooeyParser


parser = GooeyParser()

parser.add_argument('--textfield', default=2, widget="TextField")
parser.add_argument('--textarea', default="oneline twoline", widget='Textarea')
parser.add_argument('--password', default="hunter42", widget='PasswordField')
parser.add_argument('--commandfield', default="cmdr", widget='CommandField')
parser.add_argument('--dropdown', choices=["one", "two"], default="two", widget='Dropdown')
parser.add_argument(
    '--listboxie',
    nargs='+',
    default=['three', 'four'],
    choices=['one', 'two', 'three', 'four'],
    widget='Listbox',
    gooey_options={
        'height': 300,
        'validate': '',
        'heading_color': '',
        'text_color': '',
        'hide_heading': True,
        'hide_text': True,
    }
)
parser.add_argument('--counter', default=3, action='count', widget='Counter')
parser.add_argument("--overwrite1", action="store_true", default=True, widget='CheckBox')
parser.add_argument("--overwrite2", action="store_true", default=True, widget='BlockCheckbox')

verbosity = parser.add_mutually_exclusive_group(
    gooey_options={
        'initial_selection': 0
    }
)
verbosity.add_argument('--mutexone', default='hello')

parser.add_argument('--mutextwo', default='3', widget='Slider')
parser.add_argument('--mutextwo', default='1', widget='IntegerField')
parser.add_argument('--mutextwo', default='4', widget='DecimalField')

parser.add_argument("--filechooser", default="fc-value", widget='FileChooser')
parser.add_argument("--filesaver", default="fs-value", widget='FileSaver')
parser.add_argument("--dirchooser", default="dc-value", widget='DirChooser')
parser.add_argument("--datechooser", default="2015-01-01", widget='DateChooser')
parser.add_argument("--colourchooser", default="#000000", widget='ColourChooser')



