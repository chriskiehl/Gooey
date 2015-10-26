import re


def maybe_quote(string):
  return u'"{}"'.format(string) if not re.match(r'^".*"$', string) else string
