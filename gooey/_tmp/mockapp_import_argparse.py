'''
Created on Dec 21, 2013

@author: Chris
'''
import sys
import hashlib
from time import time as _time
from time import sleep as _sleep
import argparse

from gooey import Gooey


def main():
  my_cool_parser = argparse.ArgumentParser(description="Mock application to test Gooey's functionality")
  my_cool_parser.add_argument("filename", help="Name of the file you want to read")  # positional
  my_cool_parser.add_argument("outfile", help="Name of the file where you'll save the output")  # positional
  my_cool_parser.add_argument('-c', '--countdown', default=10, type=int, help='sets the time to count down from')
  my_cool_parser.add_argument("-s", "--showtime", action="store_true", help="display the countdown timer")
  my_cool_parser.add_argument("-d", "--delay", action="store_true", help="Delay execution for a bit")
  my_cool_parser.add_argument('--verbose', '-v', action='count')
  my_cool_parser.add_argument("-o", "--obfuscate", action="store_true", help="obfuscate the countdown timer!")
  my_cool_parser.add_argument('-r', '--recursive', choices=['yes', 'no'], help='Recurse into subfolders')
  my_cool_parser.add_argument("-w", "--writelog", default="No, NOT whatevs", help="write log to some file or something")
  my_cool_parser.add_argument("-e", "--expandAll", action="store_true", help="expand all processes")

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

# 	raise ValueError("Something has gone wrong! AHHHHHHHHHHH")

if __name__ == '__main__':
  # 	sys.argv.extend('asdf -c 5 -s'.split())
  # 	print sys.argv
  main()