"""
Example program to demonstrate Gooey's presentation of subparsers
"""

from gooey import Gooey, GooeyParser

@Gooey(
    optional_cols=2,
    program_name="Subparser Demo",
    dump_build_config=True,
    show_success_modal=False)
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
    time.sleep(.6)
    for i in dest_vars:
        assert getattr(args, i) is not None
    print("Success")


def get_parser():
    parser = GooeyParser()
    subs = parser.add_subparsers(help='commands', dest='command')

    parser_one = subs.add_parser('parser1', prog="Parser 1")
    parser_one.add_argument('--textfield', default=2, widget="TextField")
    parser_one.add_argument('--textarea', default="oneline twoline",
                            widget='Textarea')
    parser_one.add_argument('--password', default="hunter42",
                            widget='PasswordField')
    parser_one.add_argument('--commandfield', default="cmdr",
                            widget='CommandField')
    parser_one.add_argument('--dropdown',
                            choices=["one", "two"], default="two",
                            widget='Dropdown')
    parser_one.add_argument('--listboxie',
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
                            }
                            )
    parser_one.add_argument('-c', '--counter', default=3, action='count',
                            widget='Counter')
    #
    parser_one.add_argument("-o", "--overwrite", action="store_true",
                            default=True,
                            widget='CheckBox')

    ### Mutex Group ###
    verbosity = parser_one.add_mutually_exclusive_group(
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

    parser_one.add_argument("--filechooser", default="fc-value", widget='FileChooser')
    parser_one.add_argument("--filesaver", default="fs-value", widget='FileSaver')
    parser_one.add_argument("--dirchooser", default="dc-value", widget='DirChooser')
    parser_one.add_argument("--datechooser", default="2015-01-01", widget='DateChooser')

    parser_two = subs.add_parser('parser2', prog="parser 2")
    parser_two.add_argument('--textfield', default=2, widget="TextField")
    parser_two.add_argument('--textarea', default="oneline twoline", widget='Textarea')
    parser_two.add_argument('--password', default="hunter42", widget='PasswordField')
    parser_two.add_argument('--commandfield', default="cmdr", widget='CommandField')
    parser_two.add_argument('--dropdown', choices=["one", "two"], default="two", widget='Dropdown')
    parser_two.add_argument('--listboxie',
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
                            }
                            )
    parser_two.add_argument('-c', '--counter', default=3, action='count', widget='Counter')
    parser_two.add_argument("-o", "--overwrite", action="store_true", default=True, widget='CheckBox')

    ### Mutex Group ###
    verbosity = parser_two.add_mutually_exclusive_group(
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

    parser_two.add_argument("--filechooser", default="fc-value", widget='FileChooser')
    parser_two.add_argument("--filesaver", default="fs-value", widget='FileSaver')
    parser_two.add_argument("--dirchooser", default="dc-value", widget='DirChooser')
    parser_two.add_argument("--datechooser", default="2015-01-01", widget='DateChooser')

    return parser

if __name__ == '__main__':
    main()
