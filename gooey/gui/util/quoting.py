import sys


if sys.platform.startswith("win"):
  def quote(value):
    return u'"{}"'.format(u'{}'.format(value).replace(u'"', u'""'))
else:  # POSIX shell
  def quote(value):
    return u"'{}'".format(u'{}'.format(value).replace(u"'", u"'\\''"))

