'''
Created on Feb 2, 2014

@author: Chris
'''
import time
from gooey import Gooey

def main():
  end = time.time() + 10
  while end > time.time():
    print 'Jello!', time.time()
    time.sleep(.8)


if __name__ == '__main__':
  main()

