"""
Example program to demonstrate Gooey's presentation of subparsers
"""

import argparse

from gooey import Gooey, GooeyParser
from gooey.examples import display_message

running = True


@Gooey(optional_cols=2, program_name="Subparser Demo")
def main():
  settings_msg = 'Subparser example demonstating bundled configurations ' \
                 'for Siege, Curl, and FFMPEG'
  parser = GooeyParser(description=settings_msg)
  parser.add_argument('--verbose', help='be verbose', dest='verbose',
                      action='store_true', default=False)
  subs = parser.add_subparsers(help='commands', dest='command')

  curl_parser = subs.add_parser('curl', help='curl is a tool to transfer data from or to a server')
  curl_parser.add_argument('Path',
                           help='URL to the remote server',
                           type=str, widget='FileChooser')
  curl_parser.add_argument('--connect-timeout',
                           help='Maximum time in seconds that you allow curl\'s connection to take')
  curl_parser.add_argument('--user-agent',
                           help='Specify the User-Agent string ')
  curl_parser.add_argument('--cookie',
                           help='Pass the data to the HTTP server as a cookie')
  curl_parser.add_argument('--dump-header', type=argparse.FileType,
                           help='Write the protocol headers to the specified file')
  curl_parser.add_argument('--progress-bar', action="store_true",
                           help='Make curl display progress as a simple progress bar')
  curl_parser.add_argument('--http2', action="store_true",
                           help='Tells curl to issue its requests using HTTP 2')
  curl_parser.add_argument('--ipv4', action="store_true",
                           help=' resolve names to IPv4 addresses only')



  # ########################################################
  siege_parser = subs.add_parser('siege', help='Siege is an http/https regression testing and benchmarking utility')
  siege_parser.add_argument('--get',
                            help='Pull down headers from the server and display HTTP transaction',
                            type=str)
  siege_parser.add_argument('--concurrent',
                            help='Stress the web server with NUM number of simulated users',
                            type=int)
  siege_parser.add_argument('--time',
                            help='allows you to run the test for a selected period of time',
                            type=int)
  siege_parser.add_argument('--delay',
                            help='simulated user is delayed for a random number of seconds between one and NUM',
                            type=int)
  siege_parser.add_argument('--message',
                            help='mark the log file with a separator',
                            type=int)


  # ########################################################
  ffmpeg_parser = subs.add_parser('ffmpeg', help='Siege is an http/https regression testing and benchmarking utility')
  ffmpeg_parser.add_argument('Output',
                             help='Pull down headers from the server and display HTTP transaction',
                             widget='FileSaver', type=argparse.FileType)
  ffmpeg_parser.add_argument('--bitrate',
                             help='set the video bitrate in kbit/s (default = 200 kb/s)',
                             type=str)
  ffmpeg_parser.add_argument('--fps',
                             help='set frame rate (default = 25)',
                             type=str)
  ffmpeg_parser.add_argument('--size',
                             help='set frame size. The format is WxH (default 160x128)',
                             type=str)
  ffmpeg_parser.add_argument('--aspect',
                             help='set aspect ratio (4:3, 16:9 or 1.3333, 1.7777)',
                             type=str)
  ffmpeg_parser.add_argument('--tolerance',
                             help='set video bitrate tolerance (in kbit/s)',
                             type=str)
  ffmpeg_parser.add_argument('--maxrate',
                             help='set min video bitrate tolerance (in kbit/s)',
                             type=str)
  ffmpeg_parser.add_argument('--bufsize',
                             help='set ratecontrol buffere size (in kbit)',
                             type=str)

  parser.parse_args()

  display_message()




if __name__ == '__main__':
  main()
