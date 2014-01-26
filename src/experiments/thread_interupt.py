'''
Created on Jan 26, 2014

@author: Chris
'''

import time
import threading
from multiprocessing import Process

class MyClass(threading.Thread):
	'''
	classdocs
	'''
	def __init__(self):
		threading.Thread.__init__(self)
		self.start_time = time.time()  

	def run(self):
		while time.time() - self.start_time < 10:
			pass
		
	def throw_exception(self):
		raise KeyboardInterrupt
		
		
if __name__ == '__main__':
	a = MyClass() 
	a.start() 
	
	time.sleep(2)
	a.exit()
	time.sleep(2)
	print a.is_alive()

	a.join()
	
	
			