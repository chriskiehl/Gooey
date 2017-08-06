from rx.subjects import Subject


class StateContainer(Subject):
  """
  Python dict as an RxPy Subject
  """
  def __init__(self, initialState=None):
    super(StateContainer, self).__init__()
    self._state = initialState or {}

  def __getitem__(self, item):
    return self._state[item]

  def __setitem__(self, key, value):
    self._state[key] = value
    self.on_next(self._state)
