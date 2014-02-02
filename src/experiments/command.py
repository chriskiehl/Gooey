
'''
Created on Jan 7, 2014

@author: Chris
'''

import sys
import time
from itertools import izip_longest

def doo(x):
	print x 
	
def foo(x):
	print x 
	
def zoo():
	print 'zoo'
	
def coo():
	print 'coo'

msgs = [[
				'msg1',
				'msg2'
			],[
				'msg3', 
				'msg4'
			]]

commands = [[
						doo,
						foo, 
						zoo, 
						coo
					],[
						doo,
						foo, 
						zoo, 
						coo
					]]

_msgs = iter(msgs)
_cmds = iter(commands)

for i in izip_longest(next(_msgs), next(_cmds), fillvalue=None):
	print i








