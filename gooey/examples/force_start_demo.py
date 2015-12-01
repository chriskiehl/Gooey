'''
Created on Feb 2, 2014

@author: Chris
'''
from __future__ import print_function
import time
from gooey import Gooey

@Gooey
def main():
  end = time.time() + 3
  while end > time.time():
    print('Hello!', time.time())
    time.sleep(.8)


if __name__ == '__main__':
  main()

