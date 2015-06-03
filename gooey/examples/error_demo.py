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


@Gooey
def main():
  desc = "Example application to show Gooey's various widgets"
  my_cool_parser = GooeyParser(description=desc)
  my_cool_parser.add_argument("Example", help="fill ", widget="FileChooser")   # positional
  verbosity = my_cool_parser.add_mutually_exclusive_group()
  verbosity.add_argument('-t', '--verbozze', dest='verbose', action="store_true", help="Show more details")
  verbosity.add_argument('-q', '--quiet', dest='quiet', action="store_true", help="Only output on error")
  print my_cool_parser._actions
  print 'inside of main(), my_cool_parser =', my_cool_parser

  args = my_cool_parser.parse_args()
  print sys.argv
  print args.countdown
  print args.showtime

  start_time = _time()
  print 'Counting down from %s' % args.countdown
  while _time() - start_time < args.countdown:
    if args.showtime:
      print 'printing message at: %s' % _time()
    else:
      print 'printing message at: %s' % hashlib.md5(str(_time())).hexdigest()
    _sleep(.5)
  print 'Finished running the program. Byeeeeesss!'

def here_is_smore():
  pass


if __name__ == '__main__':
  print sys.argv
  main()
  # import inspect
  # import dis
  # # print dir(main.__code__)
  # # for i in dir(main.__code__):
  # #   print i, getattr(main.__code__, i)
  # print dis.dis(main.__code__)
  # # for i in inspect.getmembers(main):
  # #   print i
