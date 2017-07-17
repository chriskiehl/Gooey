import sys
import os
import signal


if sys.platform.startswith("win"):
  def taskkill(pid):
    os.system('taskkill /F /PID {:d} /T >NUL 2>NUL'.format(pid))
else:  # POSIX
  import psutil
  def taskkill(pid):
    parent = psutil.Process(pid)
    for child in parent.children(recursive=True):
      child.kill()
    parent.kill()
