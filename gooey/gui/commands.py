import itertools
import docopt
from gooey.python_bindings import argparse_to_json


class Required(object):
  def __init__(self, id):

class Optional(object):
  pass







parser = []

command_list = CommandList(argparse_to_json.convert(parser))

print command_list.required_args
command_list['filter'].value = 123
command_list['compress'].value = True

if not command_list.is_valid():
  raise "invalid"



