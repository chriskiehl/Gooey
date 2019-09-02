from gooey import Gooey
from gooey import GooeyParser


@Gooey(
    sidebar_title="Your Custom Title",
    show_sidebar=True,
    dump_build_config=True,
    show_success_modal=False,
    force_stop_is_error=False,
    language='chinese'
)
def main():
    dest_vars = [
        'textfield',
        'textarea',
        'password',
        'commandfield',
        'dropdown',
        'listboxie',
        'counter',
        'overwrite',
        'mutextwo',
        'filechooser',
        'filesaver',
        'dirchooser',
        'datechooser'

    ]

    parser = get_parser()
    args = parser.parse_args()
    import time
    for i in dest_vars:
        assert getattr(args, i) is not None
    print("Success")



def get_parser():
    desc = "Example application to show Gooey's various widgets"
    parser = GooeyParser(description=desc, add_help=False)

    parser.add_argument('--textfield', default=2, widget="TextField")
    parser.add_argument('--textarea', default="oneline twoline", widget='Textarea')
    parser.add_argument('--password', default="hunter42", widget='PasswordField')
    parser.add_argument('--commandfield', default="cmdr", widget='CommandField')
    parser.add_argument('--dropdown', choices=["one", "two"], default="two", widget='Dropdown')
    parser.add_argument('--listboxie',
                        nargs='+',
                        default=['Option three', 'Option four'],
                        choices=['Option one', 'Option two', 'Option three',
                                 'Option four'],
                        widget='Listbox',
                        gooey_options={
                            'height': 300,
                            'validate': '',
                            'heading_color': '',
                            'text_color': '',
                            'hide_heading': True,
                            'hide_text': True,
                        })
    parser.add_argument('-c', '--counter', default=3, action='count', widget='Counter')
    parser.add_argument("-o", "--overwrite", action="store_true", default=True, widget='CheckBox')
    parser.add_argument("-bo", "--blockcheckbox", action="store_true", default=True, widget='BlockCheckbox')

    ### Mutex Group ###
    verbosity = parser.add_mutually_exclusive_group(
        required=True,
        gooey_options={
            'initial_selection': 1
        }
    )
    verbosity.add_argument(
        '--mutexone',
        default=True,
        action='store_true',
        help="Show more details")

    verbosity.add_argument(
        '--mutextwo',
        default='mut-2',
        widget='TextField')

    parser.add_argument("--filechooser", default="fc-value", widget='FileChooser')
    parser.add_argument("--filesaver", default="fs-value", widget='FileSaver')
    parser.add_argument("--dirchooser", default="dc-value", widget='DirChooser')
    parser.add_argument("--datechooser", default="2015-01-01", widget='DateChooser')
    parser.add_argument("--multidirchooser", default="2015-01-01", widget='MultiDirChooser')

    return parser

if __name__ == '__main__':
    main()
