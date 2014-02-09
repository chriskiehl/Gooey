'''
Created on Dec 9, 2013

@author: Chris
'''

# import Queue 
# 
# q = Queue.Queue()
# 
# q.get(timeout=5)


class A(object):
			
	def __init__(self):
		self.value = 'a'
		self.value2 = A.B()
		 
	class B(object):
		def __init__(self):
			self.value = 'asdfasdf'
		
		def asdf(self):
			print 'I was called!'
			
		
		
# a = A()
# print a.value
# print a.value2.asdf()  
	
a = 'asdf.now()'
print 'asdf' in a
