import time

from gooey import Gooey
from gooey import GooeyParser


@Gooey(
    sidebar_title="Your Custom Title",
    show_sidebar=True,
    show_success_modal=False,
    force_stop_is_error=False,
)
def main():
    parser = get_parser()
    args = parser.parse_args()
    time.sleep(2)
    print("Success")


def get_parser():
    """
    A simple parser with a single required argument and no default thus
    ensuring that clicking the start button in the UI will throw
    a validation error.
    """
    desc = "Example application to show Gooey's various widgets"
    parser = GooeyParser(description=desc, add_help=False)
    parser.add_argument('--textfield', widget="TextField", required=True)
    return parser


if __name__ == '__main__':
    main()