import sys

from gooey import Gooey
from gooey import GooeyParser
from argparse import ArgumentParser

@Gooey(
    progress_regex=r"^progress: (-?\d+)%$",
    disable_progress_bar_animation=True,
    dump_build_config=True,
    show_success_modal=False,
    auto_start=True
)
def main():
    parser = get_parser()
    _ = parser.parse_args(sys.argv[1:])
    import time
    time.sleep(2)
    print('Success')



def get_parser():
    return GooeyParser(prog="example_progress_bar_1")

if __name__ == '__main__':
    main()
