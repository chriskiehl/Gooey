'''
Created on Jan 25, 2014

@author: Chris
'''

import os 
import sys 
import json

class I18N(object):
	'''
	Provides Internationalization for all text within the 
	program.
	'''
	_instance = None
	_default_dir = os.path.join(os.path.dirname(__file__), 'languages')  
	def __init__(self, language='english'):
		''' Create an I18N object '''
		self._dict = self._open(self._get_path(language))
		
	def __new__(cls, *a, **kw):
		if cls._instance is None:
			cls._instance = super(I18N, cls).__new__(cls, *a, **kw)
		return cls._instance
		
	def _get_path(self, language):
		''' Returns the full path to the language file '''
		if os.path.exists(language):
			# user supplied a custom path
			if not language.endswith('.json'):
				raise ValueError('Language packs must be in json format')
			return language
		else:
			lang_path = os.path.join(self._default_dir, language + '.json')
			return lang_path
		
	def _open(self, path):
		''' Open and return the supplied json file '''
		try:
			with open(path.lower(), 'rb') as f:
				return json.load(f)
		except IOError: 
			raise IOError('Language file not found. Make sure that your ',
									'translation file is in the languages directory, ',
									'or that your path is correct (if passing one in explicitly)')
		
	def __getitem__(self, item):
		return self._dict[item]
		
			
if __name__ == '__main__':
	pass

	
	
	