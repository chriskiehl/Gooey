"""
Python file for Processor test suite

Short 1s loop which purposefully ignores
Keyboard Interrupts in order to continue
executing
"""

import time
import signal
end = time.time() + 0.5

while time.time() < end:
    try:
        print(time.time())
        time.sleep(0.01)
    except KeyboardInterrupt:
        # Ignored!
        print("You ain't stoppin me, fool")
