import psutil


def taskkill(pid):
  proc = psutil.Process(pid)
  for child in proc.children(recursive=True):
    child.kill()
  proc.kill()
