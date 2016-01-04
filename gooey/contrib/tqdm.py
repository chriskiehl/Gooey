from __future__ import print_function
from __future__ import absolute_import

import sys

from tqdm import *
from tqdm import __all__ as _tqdm__all__
from tqdm import tqdm as _orig_tqdm
from tqdm import trange as _orig_trange

from gooey.gui.util.gooeyed import gooeyed as _gooeyed


__all__ = ["RE_TQDM", ] + list(_tqdm__all__)


RE_TQDM = r'^ {0,2}(\d+)% \d+/\d+ \[.+\]$'


class _IOWrapper(object):
  def write(self, s):
    if s == "\n":
      return
    sys.stderr.write(s.replace("\r", "").rstrip("\n"))
    sys.stderr.write("\n")

  def flush(self):
    sys.stderr.flush()


class _IODummy(object):
  def write(self, s):
    pass

  def flush(self):
    pass


def _get_tqdm_kwargs(kwargs):
  kwargs = kwargs.copy()
  kwargs.pop("desc", None)
  kwargs.pop("bar_format", None)
  kwargs["ncols"] = 0
  kwargs["dynamic_ncols"] = False
  kwargs["leave"] = True
  kwargs["ascii"] = True
  if kwargs.get("nested", False):
    kwargs["file"] = _IODummy()
  else:
    kwargs["file"] = _IOWrapper()
  return kwargs


def tqdm(iterable, **kwargs):
  if _gooeyed():
    kwargs = _get_tqdm_kwargs(kwargs)
  return _orig_tqdm(iterable, **kwargs)


def trange(*args, **kwargs):
  if _gooeyed():
    kwargs = _get_tqdm_kwargs(kwargs)
  return _orig_trange(*args, **kwargs)
