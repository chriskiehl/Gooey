"""
Python file for Processor test suite

Infinite loop which would continue forever if not
interrupted.
"""
import time
import sys

if sys.platform.startswith('win'):
    import ctypes
    kernel32 = ctypes.WinDLL('kernel32')
    kernel32.SetConsoleCtrlHandler(None, 0)


while True:
    print(time.time())
    time.sleep(0.1)