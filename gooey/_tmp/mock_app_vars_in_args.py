__author__ = 'Chris'

from argparse import ArgumentParser
from gooey import Gooey


def main():
    """Main"""
    bar = 'bar'
    parser = ArgumentParser(description='Desc')
    parser.add_argument('bar', help=('bar'))    ##################
    args = parser.parse_args()
    print(args)
    return True


if __name__ == '__main__':
  main()