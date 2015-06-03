'''
Created on Dec 21, 2013

@author: Chris
'''

from gooey import Gooey
from gooey import GooeyParser
from gooey.examples import display_message

welcome_message = \
r'''
 __          __  _
 \ \        / / | |
  \ \  /\  / /__| | ___ ___  _ __ ___   ___
   \ \/  \/ / _ \ |/ __/ _ \| '_ ` _ \ / _ \
    \  /\  /  __/ | (_| (_) | | | | | |  __/
  ___\/__\/ \___|_|\___\___/|_| |_| |_|\___|
 |__   __|
    | | ___
    | |/ _ \
    | | (_) |
   _|_|\___/                    _ _
  / ____|                      | | |
 | |  __  ___   ___   ___ _   _| | |
 | | |_ |/ _ \ / _ \ / _ \ | | | | |
 | |__| | (_) | (_) |  __/ |_| |_|_|
  \_____|\___/ \___/ \___|\__, (_|_)
                           __/ |
                          |___/
'''

@Gooey(language='japanese', program_name=u'\u30d7\u30ed\u30b0\u30e9\u30e0\u4f8b')
def arbitrary_function():
  desc = u"\u30b3\u30de\u30f3\u30c9\u30e9\u30a4\u30f3\u5f15\u6570\u3092\u5165\u529b\u3057\u3066\u304f\u3060\u3055\u3044"
  file_help_msg = u"\u51e6\u7406\u3057\u305f\u3044\u30d5\u30a1\u30a4\u30eb\u306e\u540d\u524d"
  my_cool_parser = GooeyParser(description=desc)
  my_cool_parser.add_argument(u"\u30d5\u30a1\u30a4\u30eb\u30d6\u30e9\u30a6\u30b6", help=file_help_msg, widget="FileChooser")   # positional

  my_cool_parser.add_argument('-d', u'--\u30c7\u30e5\u30ec\u30fc\u30b7\u30e7\u30f3', default=2, type=int, help=u'\u30d7\u30ed\u30b0\u30e9\u30e0\u51fa\u529b\u306e\u671f\u9593\uff08\u79d2\uff09')
  my_cool_parser.add_argument('-s', u'--\u30b9\u30b1\u30b8\u30e5\u30fc\u30eb', type=int, help=u'\u65e5\u6642\u30d7\u30ed\u30b0\u30e9\u30e0\u3092\u958b\u59cb\u3059\u3079\u304d', widget='DateChooser')
  my_cool_parser.add_argument("-c", u"--\u30b7\u30e7\u30fc\u30bf\u30a4\u30e0", action="store_true", help=u"\u30ab\u30a6\u30f3\u30c8\u30c0\u30a6\u30f3\u30bf\u30a4\u30de\u30fc\u3092\u8868\u793a\u3057\u307e\u3059")
  my_cool_parser.add_argument("-p", u"--\u30dd\u30fc\u30ba", action="store_true", help=u"\u4e00\u6642\u505c\u6b62\u306e\u5b9f\u884c")

  args = my_cool_parser.parse_args()
  main(args)


def main(args):
  display_message()

def here_is_smore():
  pass


if __name__ == '__main__':
  arbitrary_function()
