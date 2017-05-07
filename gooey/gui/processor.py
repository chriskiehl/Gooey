import os
import re
import subprocess

from functools import partial
from multiprocessing.dummy import Pool

import sys

from gooey.gui.pubsub import pub
from gooey.gui.util.casting import safe_float
from gooey.gui.util.functional import unit, bind
from gooey.gui.util.taskkill import taskkill


class ProcessController(object):
  def __init__(self, progress_regex, progress_expr):
    self._process = None
    self.progress_regex = progress_regex
    self.progress_expr = progress_expr

  def was_success(self):
    self._process.communicate()
    return self._process.returncode == 0

  def poll(self):
    if not self._process:
      raise Exception('Not started!')
    self._process.poll()

  def stop(self):
    if self.running():
      taskkill(self._process.pid)

  def running(self):
    return self._process and self.poll() is None

  def run(self, command):
    env = os.environ.copy()
    env["GOOEY"] = "1"
    try:
      self._process = subprocess.Popen(
        command.encode(sys.getfilesystemencoding()),
        bufsize=1, stdout=subprocess.PIPE, stdin=subprocess.PIPE,
        stderr=subprocess.STDOUT, shell=True, env=env)
    except:
      self._process = subprocess.Popen(
        command,
        bufsize=1, stdout=subprocess.PIPE, stdin=subprocess.PIPE,
        stderr=subprocess.STDOUT, shell=True, env=env)
    Pool(1).apply_async(self._forward_stdout, (self._process,))

  def _forward_stdout(self, process):
    '''
    Reads the stdout of `process` and forwards lines and progress
    to any interested subscribers
    '''
    while True:
      line = process.stdout.readline()
      if not line:
        break
      pub.send_message('console_update', msg=line)
      pub.send_message('progress_update', progress=self._extract_progress(line))
    pub.send_message('execution_complete')

  def _extract_progress(self, text):
    '''
    Finds progress information in the text using the
    user-supplied regex and calculation instructions
    '''
    # monad-ish dispatch to avoid the if/else soup
    find = partial(re.search, string=text.strip())
    regex = unit(self.progress_regex)
    match = bind(regex, find)
    result = bind(match, self._calculate_progress)
    return result

  def _calculate_progress(self, match):
    '''
    Calculates the final progress value found by the regex
    '''
    if not self.progress_expr:
      return safe_float(match.group(1))
    else:
      return self._eval_progress(match)

  def _eval_progress(self, match):
    '''
    Runs the user-supplied progress calculation rule
    '''
    _locals = {k: safe_float(v) for k, v in match.groupdict().items()}
    if "x" not in _locals:
      _locals["x"] = [safe_float(x) for x in match.groups()]
    try:
      return int(eval(self.progress_expr, {}, _locals))
    except:
      return None

