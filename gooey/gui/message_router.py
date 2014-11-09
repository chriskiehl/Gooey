import threading

__author__ = 'Chris'


class MessageRouter(threading.Thread):
  def __init__(self, textbox, process_to_route):
    threading.Thread.__init__(self)
    self.textbox = textbox
    self.process = process_to_route

  def run(self):
    while True:
      line = self.process.stdout.readline()
      if not line:
        break



