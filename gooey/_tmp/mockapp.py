'''
Created on Dec 21, 2013

@author: Chris
'''
import sys
import hashlib
from time import time as _time, time
from time import sleep as _sleep
# from argparse import ArgumentParser
# import argparse
import argparse as ap
from argparse import ArgumentParser as AP

from gooey import Gooey
from gooey import GooeyParser


def main():
  print 'hello'
  '''
  does stuff with parser.parse_args()
  '''
  desc = "Mock application to test Gooey's functionality"
  file_help_msg = "Name of the file you want to process"
  my_cool_parser = GooeyParser(description=desc)
  my_cool_parser.add_argument("filename", help=file_help_msg, widget="FileChooser")  # positional
  my_cool_parser.add_argument("outfile", help="Name of the file where you'll save the output")  # positional

  my_cool_parser.add_argument('-c', '--countdown', default=2, type=int, help='sets the time to count down from you see its quite simple!')
  # my_cool_parser.add_argument('-c', '--cron-schedule', default=10, type=int, help='Set the datetime when the cron should begin', widget='DateChooser')
  my_cool_parser.add_argument("-s", "--showtime", action="store_true", help="display the countdown timer")
  my_cool_parser.add_argument("-d", "--delay", action="store_true", help="Delay execution for a bit")
  my_cool_parser.add_argument('-v', '--verbose', action='count')
  my_cool_parser.add_argument("-o", "--obfuscate", action="store_true", help="obfuscate the countdown timer!")
  my_cool_parser.add_argument('-r', '--recursive', choices=['yes', 'no'], help='Recurse into subfolders')
  my_cool_parser.add_argument("-w", "--writelog", default="No, NOT whatevs", help="write log to some file or something")
  my_cool_parser.add_argument("-e", "--expandAll", action="store_true", help="expand all processes")
  # verbosity = my_cool_parser.add_mutually_exclusive_group()
  # verbosity.add_argument('-t', '--verbozze', dest='verbose', action="store_true", help="Show more details")
  # verbosity.add_argument('-q', '--quiet', dest='quiet', action="store_true", help="Only output on error")
  print my_cool_parser._actions
  print 'inside of main(), my_cool_parser =', my_cool_parser

  args = my_cool_parser.parse_args()
  print 'EHOOOOOOOOOOOO'
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
  raise ValueError("Something has gone wrong! AHHHHHHHHHHH")

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
