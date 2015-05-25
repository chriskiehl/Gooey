'''
Created on Jan 25, 2014

@author: Chris

Provides Internationalization for all text within the program.

'''

import os
import json

from gooey.gui.lang import i18n_config


__all__ = ['translate']

_LANG = i18n_config.LANG
_DEFAULT_DIR = os.path.join(os.path.dirname(__file__), '../../languages')

_DICTIONARY = None

def get_path(language):
  ''' Returns the full path to the language file '''
  filename = language.lower() + '.json'
  lang_file_path = os.path.join(_DEFAULT_DIR, filename)
  if not os.path.exists(lang_file_path):
    raise IOError('Could not find {} language file'.format(language))
  return lang_file_path


def load(filename):
  ''' Open and return the supplied json file '''
  global _DICTIONARY
  try:
    json_file = filename + '.json'
    with open(os.path.join(_DEFAULT_DIR, json_file), 'rb') as f:
      _DICTIONARY = json.load(f)
  except IOError:
    raise IOError('Language file not found. Make sure that your ',
                  'translation file is in the languages directory, ')

def translate(key):
  return _DICTIONARY[key]

def _(key):
  return _DICTIONARY[key]

if __name__ == '__main__':
  pass



