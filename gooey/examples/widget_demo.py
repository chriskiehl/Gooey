'''
Created on Dec 21, 2013
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

@author: Chris
'''

from gooey import Gooey
from gooey import GooeyParser
from gooey.examples import display_message


@Gooey(dump_build_config=True, program_name="Widget Demo")
def main():
  desc = "Example application to show Gooey's various widgets"
  file_help_msg = "Name of the file you want to process"
  my_cool_parser = GooeyParser(description=desc)
  my_cool_parser.add_argument("FileChooser", help=file_help_msg, widget="FileChooser")   # positional
  # my_cool_parser.add_argument("DirectoryChooser", help=file_help_msg, widget="DirChooser")   # positional
  # my_cool_parser.add_argument("FileSaver", help=file_help_msg, widget="FileSaver")   # positional
  my_cool_parser.add_argument("MultiFileSaver", help=file_help_msg, widget="MultiFileChooser")   # positional
  # my_cool_parser.add_argument("directory", help="Directory to store output")          # positional

  my_cool_parser.add_argument('-d', '--duration', default=2, type=int, help='Duration (in seconds) of the program output')
  my_cool_parser.add_argument('-s', '--cron-schedule', type=int, help='datetime when the cron should begin', widget='DateChooser')
  my_cool_parser.add_argument("-c", "--showtime", action="store_true", help="display the countdown timer")
  my_cool_parser.add_argument("-p", "--pause", action="store_true", help="Pause execution")
  my_cool_parser.add_argument('-v', '--verbose', action='count')
  my_cool_parser.add_argument("-o", "--overwrite", action="store_true", help="Overwrite output file (if present)")
  my_cool_parser.add_argument('-r', '--recursive', choices=['yes', 'no'], help='Recurse into subfolders')
  my_cool_parser.add_argument("-w", "--writelog", default="writelogs", help="Dump output to local file")
  my_cool_parser.add_argument("-e", "--error", action="store_true", help="Stop process on error (default: No)")
  verbosity = my_cool_parser.add_mutually_exclusive_group()
  verbosity.add_argument('-t', '--verbozze', dest='verbose', action="store_true", help="Show more details")
  verbosity.add_argument('-q', '--quiet', dest='quiet', action="store_true", help="Only output on error")

  args = my_cool_parser.parse_args()
  display_message()

def here_is_smore():
  pass


if __name__ == '__main__':
  main()
