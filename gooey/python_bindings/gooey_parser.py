
from argparse import ArgumentParser


class GooeyParser(object):
    def __init__(self, **kwargs):
      self.__dict__['parser'] = ArgumentParser(**kwargs)
      self.widgets = {}

    @property
    def _mutually_exclusive_groups(self):
      return self.parser._mutually_exclusive_groups

    @property
    def _actions(self):
      return self.parser._actions

    @property
    def description(self):
      return self.parser.description

    def add_argument(self, *args, **kwargs):
      widget = kwargs.pop('widget', None)
      self.parser.add_argument(*args, **kwargs)
      self.widgets[self.parser._actions[-1].dest] = widget

    def add_mutually_exclusive_group(self, **kwargs):
      return self.parser.add_mutually_exclusive_group(**kwargs)

    def add_argument_group(self, *args, **kwargs):
      return self.parser.add_argument_group(*args, **kwargs)

    def parse_args(self, args=None, namespace=None):
      return self.parser.parse_args(args, namespace)

    def __getattr__(self, item):
      return getattr(self.parser, item)

    def __setattr__(self, key, value):
      return setattr(self.parser, key, value)
