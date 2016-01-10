

class SubModel(object):

  def __init__(self):
    self.section_title = None


class Presenter(object):
  def __init__(self, view, model):
    self.view = view
    self.model = model


  def on_selection_change(self):
    self.view.refresh

