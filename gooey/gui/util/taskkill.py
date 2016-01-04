import os
import signal
import psutil


def _for_all_children(proc, callback):
  for child in proc.children(recursive=True):
    callback(child)


def taskkill(pid, urgency=2):
  try:
    proc = psutil.Process(pid)
  except psutil.NoSuchProcess:
    return
  if os.name == 'nt':
    urgency = 3  # no urgency option available on Windows
  if urgency <= 1:
    _for_all_children(proc, lambda p: p.send_signal(signal.SIGINT))
  elif urgency == 2:
    _for_all_children(proc, lambda p: p.terminate())
  else:
    _for_all_children(proc, lambda p: p.kill())
    proc.kill()
