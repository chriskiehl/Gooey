import os
import psutil


def gooeyed():
  gooey_env_value = os.environ.get("GOOEY")
  if not gooey_env_value:
    return False
  try:
    gooey_pid = int(gooey_env_value)
  except ValueError:
    return False
  proc = psutil.Process()
  while proc:
    if proc.pid == gooey_pid:
      return True
    proc = proc.parent()
  return False
