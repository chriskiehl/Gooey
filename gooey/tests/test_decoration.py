import unittest
from argparse import ArgumentParser
from functools import wraps

from python_bindings.types import TimingOptions


# TODO:

# def decor(f=None, *gargs, **gkwargs):
#     @wraps(f)
#     def inner(*args, **kwargs):
#         print('hello from decorator', gargs, gkwargs)
#         # choose handler
#         # monkey patch parser
#
#         return f(*args, **kwargs)
#
#     def inner2(func):
#         return decor(func, *gargs, **gkwargs)
#
#     return inner if callable(f) else inner2
#
#
# def handle_success(params):
#     def parse_args(self: ArgumentParser, args=None, namespace=None):
#         return self._original_parse_args()
#     return parse_args
#
#
# # @decor
# def main(*args, **kwargs):
#     """Hellow world!!!!!"""
#     print('sup from main', args, kwargs)
#
#     # ArgumentParser._original_parse_args = ArgumentParser.parse_args
#     # ArgumentParser.parse_args = handle_success(ArgumentParser.parse_args)
#
#     parser = ArgumentParser()
#     parser.add_argument('-f', '--foo', help='is foo')
#     subs = parser.add_subparsers()
#     sp = subs.add_parser('hh')
#     sp.add_argument('-f', '--foo', help='sp.foo')
#     print(parser.parse_args(['hh', '-f', 'asdf']))
#
#     print(TimingOptions(show_time_remaining=True, hide_time_remaining_on_complete=True).hide_time_remaining_on_complete)
#
#
#
#
# class Testie(unittest.TestCase):
#
#     def test_thing(self, **kwargs):
#         print(main(1, 2))
#         print(help(main))