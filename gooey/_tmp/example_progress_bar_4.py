#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import print_function
import sys
from time import sleep
from gooey import Gooey, GooeyParser


@Gooey(progress_regex=r"^progress: (-?\d+)%$",
       disable_progress_bar_animation=True)
def main():
    parser = GooeyParser(prog="example_progress_bar_1")
    _ = parser.parse_args(sys.argv[1:])

    print("Step 1")

    for i in range(1, 101):
        print("progress: {}%".format(i))
        sys.stdout.flush()
        sleep(0.05)

    print("Step 2")

    print("progress: -1%")  # pulse
    sys.stdout.flush()
    sleep(3)

    print("Step 3")

    for i in range(1, 101):
        print("progress: {}%".format(i))
        sys.stdout.flush()
        sleep(0.05)


if __name__ == "__main__":
    sys.exit(main())
