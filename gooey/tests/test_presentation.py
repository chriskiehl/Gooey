import sys

import pytest
import wx
from mock import MagicMock

from gooey.gui.lang import i18n
from gooey.gui.model import MyModel
from gooey.gui.presenter import Presenter
from gooey.gui.util.freeze import get_resource_path
from gooey.python_bindings import config_generator


@pytest.fixture
def build_spec(complete_parser):
  return config_generator.create_from_parser(complete_parser, sys.argv[0])

@pytest.fixture
def build_spec_subparser(subparser):
  return config_generator.create_from_parser(subparser, sys.argv[0])

@pytest.fixture
def presentation_model(build_spec):
  app = wx.App(False)
  i18n.load(get_resource_path('languages'), build_spec['language'])
  model = MyModel(build_spec)
  view = MagicMock()
  presentation = Presenter(view, model)
  return presentation

@pytest.fixture
def subparser_presentation_model(build_spec_subparser):
  app = wx.App(False)
  i18n.load(get_resource_path('languages'), 'english')
  model = MyModel(build_spec_subparser)
  view = MagicMock()
  presentation = Presenter(view, model)
  return presentation




# ----------------------------
#         Tests              #
# ----------------------------

def test_presentation_init(presentation_model):
  '''Sanity check that the primary fields are set on init '''
  presentation = presentation_model
  presentation.initialize_view()
  assert presentation.view.heading_title == presentation.model.heading_title
  assert presentation.view.heading_subtitle == presentation.model.heading_subtitle
  assert presentation.view.required_section.populate.called
  assert presentation.view.optional_section.populate.called
  # should not call when not running in column format
  assert not presentation.view.set_list_contents.called

def test_subparser_presentation_init_sets_sidebar(subparser_presentation_model):
  presentation = subparser_presentation_model
  presentation.initialize_view()
  # should be called to initialize the sidebar
  assert presentation.view.set_list_contents.called

def test_on_start_shows_err_dlg_if_missing_args(presentation_model):
  presentation = presentation_model
  presentation.initialize_view()
  presentation.on_start()
  assert presentation.view.show_missing_args_dialog.called
  presentation.view.show_missing_args_dialog.reset_mock()

  # the inverse:
  # fill the missing args
  for arg in presentation.model.required_args:
    arg.value = 'foo'
  # patch the methods we don't need
  presentation.client_runner = MagicMock()
  presentation.update_model = MagicMock()
  presentation.model.build_command_line_string = MagicMock()

  presentation.on_start()
  # should no longer show the dialog
  assert not presentation.view.show_missing_args_dialog.called







