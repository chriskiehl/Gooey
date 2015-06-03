'''
Created on Dec 21, 2013

@author: Chris
'''

import sys
import hashlib
from time import time as _time
from time import sleep as _sleep

from gooey import Gooey
from gooey import GooeyParser
from gooey.examples import display_message


@Gooey(language='russian', program_name=u'\u041f\u0440\u0438\u043c\u0435\u0440 \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u044b')
def arbitrary_function():
  desc = u"\u041f\u0440\u0438\u043c\u0435\u0440 \u043f\u0440\u0438\u043b\u043e\u0436\u0435\u043d\u0438\u044f \u002c \u0447\u0442\u043e\u0431\u044b \u043f\u043e\u043a\u0430\u0437\u0430\u0442\u044c "
  file_help_msg = u"\u0418\u043c\u044f \u0444\u0430\u0439\u043b\u0430\u002c \u043a\u043e\u0442\u043e\u0440\u044b\u0439 \u0432\u044b \u0445\u043e\u0442\u0438\u0442\u0435 \u043e\u0431\u0440\u0430\u0431\u043e\u0442\u0430\u0442\u044c"
  my_cool_parser = GooeyParser(description=desc)
  my_cool_parser.add_argument(u"\u0432\u044b\u0431\u043e\u0440\u0430\u0444\u0430\u0439\u043b\u043e\u0432", help=file_help_msg, widget="FileChooser")   # positional
  my_cool_parser.add_argument(u"\u041d\u0435\u0441\u043a\u043e\u043b\u044c\u043a\u043e \u0444\u0430\u0439\u043b\u043e\u0432 \u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c", help=file_help_msg, widget="MultiFileChooser")   # positional

  my_cool_parser.add_argument('-d', u'--\u043f\u0440\u043e\u0434\u043e\u043b\u0436\u0438\u0442\u0435\u043b\u044c\u043d\u043e\u0441\u0442\u044c', default=2, type=int, help=u'\u041f\u0440\u043e\u0434\u043e\u043b\u0436\u0438\u0442\u0435\u043b\u044c\u043d\u043e\u0441\u0442\u044c \u0028 \u0432 \u0441\u0435\u043a\u0443\u043d\u0434\u0430\u0445 \u0029 \u043d\u0430 \u0432\u044b\u0445\u043e\u0434\u0435 \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u044b')
  my_cool_parser.add_argument('-s', u'--\u043a\u0440\u043e\u043d \u002d \u0433\u0440\u0430\u0444\u0438\u043a', type=int, help=u'\u0414\u0430\u0442\u0430', widget='DateChooser')
  my_cool_parser.add_argument("-c", "--showtime", action="store_true", help="display the countdown timer")
  my_cool_parser.add_argument("-p", "--pause", action="store_true", help="Pause execution")
  my_cool_parser.add_argument('-v', '--verbose', action='count')
  my_cool_parser.add_argument("-o", "--overwrite", action="store_true", help="Overwrite output file (if present)")
  my_cool_parser.add_argument('-r', '--recursive', choices=['yes', 'no'], help='Recurse into subfolders')
  my_cool_parser.add_argument("-w", "--writelog", default="writelogs", help="Dump output to local file")
  my_cool_parser.add_argument("-e", "--error", action="store_true", help="Stop process on error (default: No)")
  verbosity = my_cool_parser.add_mutually_exclusive_group()
  verbosity.add_argument('-t', '--verbozze', dest='verbose', action="store_true", help="Show more details")
  verbosity.add_argument('-q', '--quiet', dest='quiet', action="store_true", help="Only output on error")
  # print my_cool_parser._actions
  # print 'inside of main(), my_cool_parser =', my_cool_parser

  args = my_cool_parser.parse_args()
  main(args)


def main(args):
  display_message()

def here_is_smore():
  pass


if __name__ == '__main__':
  arbitrary_function()
