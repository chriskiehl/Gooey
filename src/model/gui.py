'''
Created on Dec 9, 2013

@author: Chris
'''

import wx
import sys
import time
import Queue
import datetime
import threading
from app.dialogs.display_main import MainWindow
from app.images import image_store 



class MockApplication(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.start_time = time.time() 
	
	def run(self):
		while time.time() - self.start_time < 5: 
			print 'printing message at: %s' % time.time() 
			time.sleep(.5)
		print 'Exiting'
			
		
def decorator(main_func=None):
	def real_decorator(main_func):
		def wrapper():
			main_func()
		return wrapper
	if callable(main_func): 
		return real_decorator(main_func)
	return real_decorator

@decorator
def my_func():
	print 'inside my_func'

if __name__ == '__main__':
	

	queue = Queue.Queue()
	
	app = wx.App(False)  
	frame = MainWindow(queue)
	frame.Show(True)     # Show the frame.

# 	mock = MockApplication()
# 	mock.start()
	
	app.MainLoop()
# 	
