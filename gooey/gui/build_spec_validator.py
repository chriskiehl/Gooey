'''
Validates that the json has meaningful keys
'''

import itertools


a = {
  'required' : [
    {
      'component': 'TextField',
      'data': {
        'display_name': 'filename',
        'help_text': 'path to file you want to process',
        'command_args': ['-f', '--infile']
      }
    },
    {
      'component': 'FileChooser',
      'data': {
        'display_name': 'Output Location',
        'help_text': 'Where to save the file',
        'command_args': ['-o', '--outfile']
      }
    }
  ],
  'optional' : [
    {
      'component': 'RadioGroup',
      'data': [
        {
          'display_name': 'Output Location',
          'help_text': 'Where to save the file',
          'command_args': ['-o', '--outfile']
        }, {
          'display_name': 'Output Location',
          'help_text': 'Where to save the file',
          'command_args': ['-o', '--outfile']
        }
      ]
    }
  ]
}

VALID_WIDGETS = (
  'FileChooser',
  'DirChooser',
  'DateChooser',
  'TextField',
  'Dropdown',
  'Counter',
  'RadioGroup'
)


class MalformedBuildSpecException(Exception):
  pass

def validate(json_string):
  required = json_string.get('required')
  optional = json_string.get('optional')

  if not required or not optional:
    raise MalformedBuildSpecException("All objects must be children of 'required,' or 'optional'")

  objects = [item for key in json_string for item in json_string[key]]

  for obj in objects:
    if obj['component'] not in VALID_WIDGETS:
      raise MalformedBuildSpecException("Invalid Component name: {0}".format(obj['component']))


if __name__ == '__main__':

  validate(a)




