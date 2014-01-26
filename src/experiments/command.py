'''
Created on Jan 7, 2014

@author: Chris
'''

import types

class Fooer(object):
	def __init__(self):
		self.a=1 
		self.b=2 
		self.c=3
		
	def error(self, msg):
		print msg 
		

class Barer(object):
	def __init__(self):
		self._fooer = Fooer() 
		
	def __getattr__(self, a):
		return getattr(self._fooer, a)

class Bazzer(object):
	def __init__(self):
		self._f = Fooer()
	

def error2(self, msg):
	print 'HEY! I\'ve been patched!'
	
b = Barer() 

b.error = types.MethodType(error2, b)

b.error('asdf') 
