'''
Created on Jan 15 2019

@author: Jonathan Schultz

This file contains code that allows the default argument values to be specified
on the command line.
'''

from argparse import _SubParsersAction

def parse_cmd_args(self, args=None):

  def prepare_to_read_cmd_args(item):
    '''
    Before reading the command-line arguments, we need to fudge a few things:
      1. If there are subparsers, we need a dest in order to know in which
         subparser the command-line values should be stored.
      2. Any required argument or mutex group needs to be made not required,
         otherwise it will be compulsory to enter those values on the command
         line.
    We save the everything as it was before the fudge, so we can restore later.
    '''
    for action in item._actions:
      if isinstance(action, _SubParsersAction):
        action.save_dest = action.dest
        if not action.dest:
          action.dest = '_subparser'
      else:
        action.save_required = action.required
        action.required = False
        action.save_nargs = action.nargs
        if action.nargs == '+':
          action.nargs = '*'
        elif action.nargs is None:
          action.nargs = '?'

    for mutex_group in item._mutually_exclusive_groups:
      mutex_group.save_required = mutex_group.required
      mutex_group.required = False

  def overwrite_default_values(item, cmd_args):
    '''
    Subsistute arguments provided on the command line in the place of the
    default values provided to argparse.
    '''
    for action in item._actions:
      if isinstance(action, _SubParsersAction):
        subparser_arg = getattr(cmd_args, action.dest, None)
        if subparser_arg:
          overwrite_default_values(action.choices[subparser_arg], cmd_args)
      else:
        dest = getattr(action, 'dest', None)
        if dest:
          cmd_arg = getattr(cmd_args, dest, None)
          if cmd_arg:
            action.default = cmd_arg

  def restore_original_configuration(item):
    '''
    Restore the old values as they were to start with.
    '''
    for action in item._actions:
      if isinstance(action, _SubParsersAction):
        action.dest = action.save_dest
        del action.save_dest
      else:
        action.required = action.save_required
        del action.save_required
        action.nargs = action.save_nargs
        del action.save_nargs

    for mutex_group in item._mutually_exclusive_groups:
      mutex_group.required = mutex_group.save_required
      del mutex_group.save_required

  prepare_to_read_cmd_args(self)
  overwrite_default_values(self, self.original_parse_args(args))
  restore_original_configuration(self)
