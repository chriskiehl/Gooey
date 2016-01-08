'''
Simple monad-ish bindings
'''


def unit(val):
  return val

def bind(val, f):
  return f(val) if val else None
