'''
Main runner entry point for Gooey.
'''

import json
import sys
from collections import OrderedDict
from uuid import uuid4

from PyQt5.QtWidgets import QApplication

from copy import deepcopy

from gooey.gui.lang import i18n
from gooey.gui.state import StateContainer


def gooey1to2(buildspec):
  '''
  Still figuring out exactly how I want everything arranged..
  '''
  root_commands = OrderedDict()
  widgets = []

  for parent_name, val in buildspec['widgets'].items():
    root_commands[parent_name] = val['command']

    for index, widget in enumerate(val['contents']):
      new_widget = deepcopy(widget)
      new_widget['parent'] = parent_name
      if widget['type'] == 'MultiDirChooser':
        print('Ignoring MultiDirChooser')
        continue
      if widget['type'] == 'RadioGroup':
        print('Ignoring RadioGroup')
        continue

      if not widget['type'] == 'RadioGroup':
        if new_widget['type'] == 'DirChooser':
          new_widget['type'] = 'DirectoryChooser'
        new_widget['value'] = widget['data']['default']
      else:
        new_widget['value'] = None
      new_widget['id'] = str(uuid4())
      new_widget['order'] = index
      widgets.append(new_widget)

  widget_map = OrderedDict((widget['id'], widget) for widget in widgets)
  new_buildspec = deepcopy(buildspec)
  new_buildspec['view'] = 'configuration'
  new_buildspec['activeGroup'] = list(root_commands.keys())[0]
  new_buildspec['groups'] = root_commands
  new_buildspec['widgets'] = widget_map
  new_buildspec['title'] = 'Settings'
  new_buildspec['subtitle'] = new_buildspec['program_description']
  new_buildspec['icon'] = '../images/config_icon.png'
  new_buildspec['gooey_state'] = {
    'icon': '../images/config_icon.png',
    'title': 'Settings',
    'subtitle': new_buildspec['program_description'],
    'window': 0,
    'buttonGroup': 0
  }
  return new_buildspec


def load_initial_state():
  with open('gooey_config.json', 'r') as f:
    data = json.loads(f.read(), object_pairs_hook=OrderedDict)
    return gooey1to2(data)





# sys._excepthook = sys.excepthook


# def my_exception_hook(exctype, value, traceback):
#   # Print the error and traceback
#   print(exctype, value, traceback)
#   # Call the normal Exception hook after
#   sys._excepthook(exctype, value, traceback)
#   sys.exit(1)
#
# # Set the exception hook to our wrapping function
# sys.excepthook = my_exception_hook


def run(build_spec):
  state = StateContainer(gooey1to2(build_spec))
  i18n.load(state['language_dir'], state['language'])
  from gooey.gui.containers.application import MainWindow

  app = QApplication(sys.argv)
  form = MainWindow(state)

  state['title'] = 'Foobar'
  state['title'] = 'Settings'
  state['icon'] = '../images/config_icon.png'

  # show
  form.show()

  app.exec_()


