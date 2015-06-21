import re


def maybe_quote(string):
  return '"{}"'.format(string) if not re.match(r'^".*"$', string) else string
