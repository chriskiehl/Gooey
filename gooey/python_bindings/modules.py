
import os
import time
import hashlib
from itertools import dropwhile
import sys
import tempfile

sys.path.append(os.path.dirname(__file__))

def load(module_source):
  descriptor, tmpfilepath = tempfile.mkstemp(suffix='.py')

  tmpfiledir = os.path.dirname(tmpfilepath)
  tmpfilename = os.path.splitext(os.path.split(tmpfilepath)[-1])[0]

  sys.path.append(tmpfiledir)
  try:
    with open(tmpfilepath, 'w') as f:
      f.write(module_source)
    return __import__(tmpfilename)
  finally:
    os.close(descriptor)
    os.remove(tmpfilepath)

if __name__ == '__main__':
  pass

