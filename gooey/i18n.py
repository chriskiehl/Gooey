'''
Created on Jan 25, 2014

@author: Chris

Provides Internationalization for all text within the program.

'''

import os
import json
import i18n_config

__all__ = ['translate']

_LANG = i18n_config.LANG
_DEFAULT_DIR = os.path.join(os.path.dirname(__file__), 'languages')

def get_path(language):
  ''' Returns the full path to the language file '''
  filename = language + '.json'
  lang_file_path = os.path.join(_DEFAULT_DIR, filename)
  if not os.path.exists(lang_file_path):
    raise IOError('Could not find {} language file'.format(language))
  return lang_file_path


def load(filepath):
  ''' Open and return the supplied json file '''
  try:
    with open(filepath.lower(), 'rb') as f:
      return json.load(f)
  except IOError:
    raise IOError('Language file not found. Make sure that your ',
                  'translation file is in the languages directory, ')

_DICTIONARY = load(get_path(_LANG))

def translate(key):
  return _DICTIONARY[key]

if __name__ == '__main__':
  pass



