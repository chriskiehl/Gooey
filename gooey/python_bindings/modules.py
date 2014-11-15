__author__ = 'Chris'

import os
import time
import hashlib
from itertools import dropwhile
import sys

sys.path.append(os.path.dirname(__file__))

def generate_pyfilename():
  '''
  generates a random filename by hashing the current time stamp
  Leading numbers are dropped from the filename for import compatibility
  '''
  hash = hashlib.md5(str(time.time())).hexdigest()
  return ''.join(dropwhile(lambda c: c.isdigit(), hash))

def load(module_source):
  tmp_filename = generate_pyfilename()
  tmp_filedir = os.path.dirname(__file__)
  tmp_filepath = os.path.join(tmp_filedir, tmp_filename)

  tmp_py_file = tmp_filepath + '.py'
  tmp_pyc_file = tmp_filepath + '.pyc'

  try:
    with open(tmp_py_file, 'w') as f:
      f.write(module_source)
    return __import__(tmp_filename)
  finally:
    os.remove(tmp_py_file)
    os.remove(tmp_pyc_file)

if __name__ == '__main__':
  pass

