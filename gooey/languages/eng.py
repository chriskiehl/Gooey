'''

Simple utlity to generate the Json English language file

Created on Jan 25, 2014

@author: Chris
'''

import json


if __name__ == '__main__':
  english = {  # Header Messages
               'settings_title': 'Settings',
               'running_title': 'Running',
               'running_msg': 'Please wait while the application performs its tasks. ' +
                              '\nThis may take a few moments',
               'finished_title': 'Finished',
               'finished_msg': 'All done! You may now safely close the program.',  # Footer buttons
               'cancel': 'Cancel',
               'close': 'Close',
               'start': 'Start',  # simple config panel
               'simple_config': 'Enter Command Line Arguments',  # Advanced config panel
               'required_args_msg': 'Required Arguments',
               'optional_args_msg': 'Optional Arguments',  # popup dialogs
               "sure_you_want_to_exit": "Are you sure you want to exit?",
               'close_program': 'Close program?',
               'sure_you_want_to_stop': 'Are you sure you want to stop the task? ' +
                                        '\nInterruption can corrupt your data!',
               'stop_task': 'Stop task?',
               'status': 'Status',
               'uh_oh': '''
Uh oh! Looks like there was a problem.
Copy the text from status window to let your developer know what went wrong.
''',
               'error_title': "Error",
               'terminated': 'The task has been terminated by user.',
               'execution_finished': 'Execution finished',
               'success_message': 'Program completed sucessfully!',

  }

  with open('english.json', 'wb') as f:
    f.write(json.dumps(english, indent=4, sort_keys=True))
