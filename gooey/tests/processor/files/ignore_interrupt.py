"""
Python file for Processor test suite

Infinite loop which purposefully ignores
Keyboard Interrupts in order to continue
executing. The only way to kill it is via
SIGTERM family signals.
"""

import time
import signal
end = time.time() + 0.5

while True:
    try:
        print(time.time())
        time.sleep(0.1)
    except KeyboardInterrupt:
        # Ignored!
        print("INTERRUPT")
