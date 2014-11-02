"""inline"""

import argparse
from __builtin__ import getattr
from gooey import Gooey

x = '''random line'''

y = """
Buncha text here
and here
and here
and here
"""

# @Gooey
def main():
  """
  This is my main module
  example:
  args = parser.parse_args()
  """
  parser = argparse.ArgumentParser('Get my users')
  verbosity = parser.add_mutually_exclusive_group()
  verbosity.add_argument('-v', '--verbose', dest='verbose', action="store_true", help="Show more details")
  verbosity.add_argument('-q', '--quiet', dest='quiet', action="store_true", help="Only output on error")
  parser.add_argument("filename", help="yo yo yo")  # positional
  parser.add_argument("outfile", help="Name of the file where you'll save the output")  # positional
  slervocity = parser.add_mutually_exclusive_group()
  slervocity.add_argument('-c', '--countdown', action="store_true", help='sets the time to count down from')
  slervocity.add_argument("-s", "--showtime", action="store_true", help="display the countdown timer")
  parser.add_argument("-d", "--delay", action="store_true", help="Delay execution for a bit")
  parser.add_argument("-o", "--obfuscate", action="store_true", help="obfuscate the countdown timer!")
  parser.add_argument('-r', '--recursive', choices=['yes', 'no'], help='Recurse into subfolders')
  parser.add_argument("-w", "--writelog", default="No, NOT whatevs", help="write log to some file or something")
  parser.add_argument("-e", "--expandAll", action="store_true", help="expand all processes")

  mutually_exclusive_group = [mutex_action
                              for group_actions in parser._mutually_exclusive_groups
                              for mutex_action in group_actions._group_actions]

  base_actions = [action for action in parser._actions
                  if action not in mutually_exclusive_group]

  for i in base_actions:
    print 'Base Action:', i.option_strings
  #
  # print

  for i in mutually_exclusive_group:
    print 'Mute Action:', i

  # for i in base_actions:
  #   print dir(i)
  #   print i.nargs
  #   break


def moo(asdf):
  '''single quoted inline comment'''
  a = 1

def foo():
  """Double quoted inline comment """
  a = 1

def bar():
  """
  Double quoted
  multiline comment
  """
  a = 1

def baz():
  '''
  Double quoted
  multiline comment
  '''
  a = 1


def foo():
  parser = argparse.ArgumentParser()
  bar = 1
  baz = 2

if __name__ == '__main__':
  main()

