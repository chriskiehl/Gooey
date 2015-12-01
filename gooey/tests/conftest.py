import argparse
import pytest

@pytest.fixture
def empty_parser():
  return argparse.ArgumentParser(description='description')


@pytest.fixture
def complete_parser():
  parser = argparse.ArgumentParser(description='description')
  parser.add_argument("req1", help='filename help msg')  # positional
  parser.add_argument("req2", help="Name of the file where you'll save the output")  # positional
  parser.add_argument('-r',   dest="req3", default=10, type=int, help='sets the time to count down from', required=True)
  parser.add_argument('--req4', dest="req4", default=10, type=int, help='sets the time to count down from', required=True)

  parser.add_argument("-a", "--aa", action="store_true", help="aaa")
  parser.add_argument("-b", "--bb", action="store_true", help="bbb")
  parser.add_argument('-c', '--cc', action='count')
  parser.add_argument("-d", "--dd", action="store_true", help="ddd")
  parser.add_argument('-e', '--ee', choices=['yes', 'no'], help='eee')
  parser.add_argument("-f", "--ff", default="0000", help="fff")
  parser.add_argument("-g", "--gg", action="store_true", help="ggg")
  verbosity = parser.add_mutually_exclusive_group()
  verbosity.add_argument('-i', '--ii', action="store_true", help="iii")
  verbosity.add_argument('-j', '--jj', action="store_true", help="hhh")
  return parser


@pytest.fixture
def subparser():
  parser = argparse.ArgumentParser(description='qidev')
  parser.add_argument('--verbose', help='be verbose', dest='verbose', action='store_true', default=False)
  subs = parser.add_subparsers(help='commands', dest='command')

  config_parser = subs.add_parser('config', help='configure defaults for qidev')
  config_parser.add_argument('field', help='the field to configure', type=str)
  config_parser.add_argument('value', help='set field to value', type=str)

  # ########################################################
  connect_parser = subs.add_parser('connect', help='connect to a robot (ip/hostname)')
  connect_parser.add_argument('hostname', help='hostname or IP address of the robot', type=str)

  # ########################################################
  install_parser = subs.add_parser('install', help='package and install a project directory on a robot')
  install_parser.add_argument('path', help='path to the project directory (containing manifest.xml', type=str)
  install_parser.add_argument('--ip', nargs='*', type=str, dest='ip', help='specify hostname(es)/IP address(es)')
  return parser


@pytest.fixture
def exclusive_group():
  parser = argparse.ArgumentParser(description='description')
  verbosity = parser.add_mutually_exclusive_group()
  verbosity.add_argument('-i', dest="option1", action="store_true", help="iii")
  verbosity.add_argument('-j', dest="option2", action="store_true", help="hhh")

  mutually_exclusive_group = [mutex_action
                              for group_actions in parser._mutually_exclusive_groups
                              for mutex_action in group_actions._group_actions]
  return mutually_exclusive_group


@pytest.fixture
def expected_attrs():
  return ('program_icon', 'success_icon', 'running_icon',
          'loading_icon', 'config_icon', 'error_icon')
