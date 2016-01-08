

def safe_int(n):
  return _safe_cast(int, n)

def safe_float(n):
  return _safe_cast(float, n)


def _safe_cast(_type, val):
  try:
    return _type(val)
  except ValueError:
    return None

