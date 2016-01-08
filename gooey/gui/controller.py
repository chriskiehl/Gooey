from gooey.gui.model import MyModel
from gooey.gui.presenter import Presenter
from gooey.gui.windows.base_window import BaseWindow


YES = 5103
NO = 5104

class Controller(object):

  def __init__(self, build_spec):
    # todo: model!
    self.build_spec = build_spec
    self.view = BaseWindow(build_spec, layout_type=self.build_spec['layout_type'])
    self.presentation = Presenter(self.view, MyModel(self.build_spec))
    self.presentation.initialize_view()


  def run(self):
    self.view.Show(True)

