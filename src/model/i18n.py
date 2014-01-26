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
	def __init__(self, language='english'):
		''' Create an I18N object '''
		self._dict = self._load(language)
		
	def __new__(cls, *a, **kw):
		if cls._instance is None:
			cls._instance = super(I18N, cls).__new__(cls, *a, **kw)
		return cls._instance
		
	def _load(self, language):
		lang_dir = os.path.join(os.getcwd(), '..', 'languages')
		lang_path = os.path.join(lang_dir, language + '.json')
		try:
			with open(lang_path.lower(), 'rb') as f:
				return json.load(f)
		except IOError: 
			raise IOError(''.join(['Language "{}" not found. Make sure that your ',
									'translation file is in the languages directory']).format(language))
	
	def __getitem__(self, item):
		return self._dict[item]
		
			
if __name__ == '__main__':
	pass

	
	
	