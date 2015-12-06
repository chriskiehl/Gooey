'''
Created on Feb 10, 2014

@author: Chris
'''


class ParserError(Exception):
  """Thrown when the parser can't find argparse functions the client code"""
  pass


class ArgumentError(Exception):
  """Thrown when the parser is supplied with an incorrect argument format"""
  pass


if __name__ == '__main__':
  pass