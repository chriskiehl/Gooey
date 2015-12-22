#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import print_function
import sys
from time import sleep
from gooey import Gooey, GooeyParser


@Gooey(progress_regex=r"^progress: (\d+)/(\d+)$",
       progress_expr="x[0] / x[1] * 100",
       disable_progress_bar_animation=True)
def main():
    parser = GooeyParser(prog="example_progress_bar_2")
    parser.add_argument("steps", type=int, default=15)
    parser.add_argument("delay", type=int, default=1)
    args = parser.parse_args(sys.argv[1:])

    for i in range(args.steps):
        print("progress: {}/{}".format(i+1, args.steps))
        sys.stdout.flush()
        sleep(args.delay)


if __name__ == "__main__":
    sys.exit(main())
