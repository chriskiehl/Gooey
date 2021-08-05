"""
Python file for Processor test suite

Short 1s loop which purposefully ignores
Keyboard Interrupts in order to continue
executing
"""

import time
import signal

def ignored_it(*args):
    print("Ignoring Ctrl+BREAK!")

signal.signal(signal.SIGBREAK, ignored_it)



end = time.time() + 0.5
while time.time() < end:
    print(time.time())
    time.sleep(0.01)
