
'''
Created on Jan 7, 2014

@author: Chris
'''

import sys
import time


from multiprocessing.dummy import Process, Pool

def myFunc():
	time.sleep(2)
	print 'whoo!'
	raise ValueError("Graaaaaaahhhhh")


if __name__ == '__main__':
	pool = Pool(1)
	try:
		pool.apply(myFunc)
	except:
		print 'Yo, shit is broken, son!'
		



