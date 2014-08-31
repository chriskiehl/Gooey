'''
Created on Feb 8, 2014

@author: Chris
'''

import types

from parser_exceptions import ArgumentError
from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
import code_prep


class MonkeyParser(object):
  '''
  Builds a parser instance from the code
  extracted from the client module.

  The instance is stored as a private variable in the
  class and all methods are delagted to it so that the
  user of the class can treat it just as a normal argparse
  instance.
  '''

  def __init__(self, source_code):
    self._parser_instance = self._build_argparser_from_client_source(source_code)
    # Monkey patch parser's `error` method so that it raises an error
    # rather than silently exiting
    self._parser_instance.error = types.MethodType(
        self._ErrorAsString,
        self._parser_instance
    )

  def _build_argparser_from_client_source(self, source_code):
    '''
    runs the client code by evaling each line.

    Example input Code:
      parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
      parser.add_argument("-r", "--recursive", dest="recurse", action="store_true", help="recurse into subfolders [default: %(default)s]")
      parser.add_argument("-v", "--verbose", dest="verbose", action="count", help="set verbosity level [default: %(default)s]")

    Method extracts the instance name (e.g. parser) from the first line,
    and instantiates it in a local variable by evaling the rest of the lines.
    Each subsequent line updates the local variable in turn.
    '''
    imports = filter(lambda x: 'gooey' not in x, code_prep.take_imports(source_code))
    arg_code = code_prep.drop_imports(source_code)
    updated_source_code = code_prep.update_parser_varname('clients_parser', arg_code)

    for _import in imports:
      exec(_import)

    first_line = updated_source_code.pop(0)
    clients_parser, assignment = code_prep.split_line(first_line)
    clients_parser = eval(assignment)

    for line in updated_source_code:
      eval(line)
    return clients_parser

  def _format_source_with_new_varname(self, new_variable_name, source):
    '''
    'injects' the client code with a known variable name so that it
    can be `eval`d and assigned to a variable in the local code.

    For example, if the client code was:
      parser = ArgumentParser(descrip...)
      parser.add_argument("-r", "--re...)
      parser.add_argument("-v", "--ve...)

    The variable "parser" would be overwritten with a custom name. e.g.
      my_parser = ArgumentParser(descrip...)
      my_parser.add_argument("-r", "--re...)
    '''
    source_code = source[:]

    first_line = source_code[0]
    client_parser_variable, statement = self._split_line(first_line)

    client_parser_variable = client_parser_variable.strip()

    for index, line in enumerate(source_code):
      source_code[index] = line.replace(client_parser_variable, new_variable_name)
    source_code.append('{0}.parse_args()'.format(new_variable_name))
    return source_code

  def _split_line(self, line):
    # Splits line at the first = sign,
    # joins everything after the first =
    # to account for additional = signs in
    # parameters
    components = line.split('=')
    var = components.pop(0)
    return var, '='.join(components)

  def __getattr__(self, attr):
    '''
    Auto-delegates everything to the ArgumentParser instance'''
    return getattr(self._parser_instance, attr)

  @staticmethod
  def _ErrorAsString(self, msg):
    '''
    Monkey patch for parser.error
    Raises an error rather than
    printing and silently exiting.
    '''
    raise ArgumentError(msg)


if __name__ == '__main__':
  pass