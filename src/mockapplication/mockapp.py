'''
Created on Dec 21, 2013

@author: Chris
'''
import sys
import hashlib 
from time import time as _time
from time import sleep as _sleep
from argparse import ArgumentParser
from model.gooey import Gooey

@Gooey
def main():
	
	my_cool_parser = ArgumentParser(description="Mock application to test @Gui's functionality")
	my_cool_parser.add_argument('filename', help="bla bla bla")
	my_cool_parser.add_argument('-c', '--countdown', default=10, type=int, help='sets the time to count down from')
	my_cool_parser.add_argument("-s", "--showtime", action="store_true", help="display the countdown timer")
	my_cool_parser.add_argument("-w", "--whatevs", default="No, NOT whatevs", help="...")
	args = my_cool_parser.parse_args()
	
	start_time = _time()
	print 'Counting down from %s' % args.countdown
	while _time() - start_time < args.countdown:
		if args.showtime:
			print 'printing message at: %s' % _time()
		else:
			print 'printing message at: %s' % hashlib.md5(str(_time())).hexdigest()
		_sleep(.5)
	print 'Finished running the program. Byeeeeesss!'
	
if __name__ == '__main__':
# 	sys.argv.extend('-c 5'.split())
	main()