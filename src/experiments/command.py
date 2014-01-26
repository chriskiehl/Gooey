
'''
Created on Jan 7, 2014

@author: Chris
'''

import sys
import time

_time = time.time 

class MessagePump(object):
	def __init__(self):
# 		self.queue = queue
		self.stdout = sys.stdout
		self.asdf = []
	
	# Overrides stdout's write method
	def write(self, text):
		self.asdf.append((text, _time()))
# 		if text != '':
# 			self.queue.put(text)
			
			
# self.queue = Queue.Queue()
_stdout = sys.stdout
sys.stdout = MessagePump()
# listener = Listener(self.queue, self.cmd_textbox)
# listener.start()

print 'hello!'
time.sleep(1)
print 'Jello!'

output = sys.stdout.asdf
sys.stdout = _stdout
for i in output:
	print i
print _time()