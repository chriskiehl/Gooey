"""
Python file for Processor test suite

Short 1s loop which purposefully ignores
Keyboard Interrupts in order to continue
executing
"""

import time
import signal

def ignored_it(*args):
    print("INTERRUPT")

signal.signal(signal.SIGBREAK, ignored_it)


while True:
    print(time.time())
    time.sleep(0.1)