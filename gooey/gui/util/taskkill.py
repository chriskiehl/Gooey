import sys
import os
import signal


if sys.platform.startswith("win"):
  def taskkill(pid):
    os.system('taskkill /F /PID {:d} /T >NUL 2>NUL'.format(pid))
else:  # POSIX
  def taskkill(pid):
    os.kill(pid, signal.SIGTERM)
