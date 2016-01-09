from gooey.gui.model import MyModel
from gooey.gui.presenter import Presenter
from gooey.gui.windows.base_window import BaseWindow


class Controller(object):

  def __init__(self, build_spec):
    self.model = MyModel(build_spec)
    self.view = BaseWindow(layout_type=self.model.layout_type)
    self.presentation = Presenter(self.view, self.model)
    self.presentation.initialize_view()


  def run(self):
    self.view.Show(True)

