"""
Python file for Processor test suite

Infinite loop which purposefully ignores
Keyboard Interrupts in order to continue
executing. The only way to kill it is via
SIGTERM family signals.
"""

import time
import sys

if sys.platform.startswith('win'):
    import ctypes
    kernel32 = ctypes.WinDLL('kernel32')
    kernel32.SetConsoleCtrlHandler(None, 0)


while True:
    try:
        print(time.time())
        time.sleep(0.1)
    except KeyboardInterrupt:
        # Ignored!
        print("INTERRUPT")
