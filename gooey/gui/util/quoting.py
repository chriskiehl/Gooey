import re
import sys


if sys.platform.startswith("win"):
  def quote(value):
    return '"{}"'.format('{}'.format(value).replace('"', '""'))
else:  # POSIX shell
  def quote(value):
    return "'{}'".format('{}'.format(value).replace("'", "'\\''"))
