'''
Created on Jan 7, 2014

@author: Chris
'''

class Command(object):
	def __init__(self):
		pass
	
	def execute(self):
		pass
	
	
class NextButton(Command):
	def execute(self):
		print "Next Button"
		
class CancelButton(Command):
	def execute(self):
		print 'Cancel button!'
		
