import sys
import os
import tqdm as _tqdm


__all__ = ("RE_TQDM", "tqdm", "trange")


RE_TQDM = r'^ {0,2}(\d+)%\|.*\|.+\[.+\]$'


class _IOWrapper(object):
  def write(self, s):
    sys.stderr.write(s.replace("\r", "").rstrip("\n"))
    sys.stderr.write("\n")

  def flush(self):
    sys.stderr.flush()


if os.environ.get("GOOEY") == "1":
  def tqdm(*args, **kwargs):
    kwargs["file"] = _IOWrapper()
    return _tqdm.tqdm(*args, **kwargs)

  def trange(*args, **kwargs):
    kwargs["file"] = _IOWrapper()
    return _tqdm.trange(*args, **kwargs)

else:
  tqdm = _tqdm.tqdm
  trange = _tqdm.trange
