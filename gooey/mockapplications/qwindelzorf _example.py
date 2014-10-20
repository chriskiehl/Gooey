"""inline"""

import argparse
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
  """This is my main module"""
  parser = argparse.ArgumentParser('Get my users')
  verbosity = parser.add_mutually_exclusive_group()
  verbosity.add_argument('-v', '--verbose', dest='verbose', action="store_true", help="Show more details")
  verbosity.add_argument('-q', '--quiet', dest='quiet', action="store_true", help="Only output on error")

  for mutex_group in parser._mutually_exclusive_groups:
    group_actions = mutex_group._group_actions
    for i, mutex_action in enumerate(mutex_group._group_actions):
      print mutex_action


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


if __name__ == '__main__':
  main()
