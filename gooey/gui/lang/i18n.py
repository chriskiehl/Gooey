'''
Created on Jan 25, 2014

@author: Chris

Provides Internationalization for all text within the program.

'''

import os
import json

__all__ = ['load', '_']

_DICTIONARY = None

def load(language_dir, filename):
  ''' Open and return the supplied json file '''
  global _DICTIONARY
  try:
    json_file = filename + '.json'
    with open(os.path.join(language_dir, json_file), 'rb') as f:
      _DICTIONARY = json.load(f)
  except IOError:
    raise IOError('{0} Language file not found at location {1}. '
                  'Make sure that your translation file is in the '
                  'listed language directory'.format(filename.title(), language_dir))

def translate(key):
  return _DICTIONARY.get(key, key)

def _(key):
  return translate(key)
