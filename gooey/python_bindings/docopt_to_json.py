
"""
Naval Fate.

Usage:
  naval_fate.py ship new <name>...
  naval_fate.py ship <name> move <x> <y> [--speed=<kn>]
  naval_fate.py ship shoot <x> <y>
  naval_fate.py mine (set|remove) <x> <y> [--moored|--drifting]
  naval_fate.py -h | --help
  naval_fate.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.
  --speed=<kn>  Speed in knots [default: 10].
  --moored      Moored (anchored) mine.
  --drifting    Drifting mine.

"""

# Standard
# choice
# counter
# flag
# mutually_exclusive
#
# types?



from docopt import docopt, Option, Argument


class MyOption(Option):
  def __init__(self, *args, **kwargs):
    self.description = kwargs.pop('description', None)
    super(MyOption, self).__init__(*args, **kwargs)


  @classmethod
  def parse(class_, option_description):
      short, long, argcount, value = None, None, 0, False
      options, _, description = option_description.strip().partition('  ')
      options = options.replace(',', ' ').replace('=', ' ')
      for s in options.split():
          if s.startswith('--'):
              long = s
          elif s.startswith('-'):
              short = s
          else:
              argcount = 1
      if argcount:
          matched = re.findall('\[default: (.*)\]', description, flags=re.I)
          value = matched[0] if matched else None
      return class_(short, long, argcount, value, description=description.strip())

  def __repr__(self):
      return 'Option(%r, %r, %r, %r, %r)' % (self.short, self.long,
                                       self.argcount, self.value, self.description)


if __name__ == '__main__':
    import sys
    a = docopt(__doc__)
    # import re
    # doc = __doc__
    # split = re.split('\n *(<\S+?>|-\S+?)', doc)[1:]
    # split = [s1 + s2 for s1, s2 in zip(split[::2], split[1::2])]
    # options = [MyOption.parse(s) for s in split if s.startswith('-')]
    # arguments = [Argument.parse(s) for s in split if s.startswith('<')]
    # #return options, arguments
    # print arguments
    # print options
    print a
    a = 10
