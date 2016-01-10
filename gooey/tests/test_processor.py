import re

from gooey.gui.processor import ProcessController


def test_extract_progress():
  # should pull out a number based on the supplied
  # regex and expression
  processor = ProcessController(r"^progress: (\d+)%$", None)
  assert processor._extract_progress('progress: 50%') == 50

  processor = ProcessController(r"total: (\d+)%$", None)
  assert processor._extract_progress('my cool total: 100%') == 100

def test_extract_progress_returns_none_if_no_regex_supplied():
  processor = ProcessController(None, None)
  assert processor._extract_progress('Total progress: 100%') == None

def test_extract_progress_returns_none_if_no_match_found():
  processor = ProcessController(r'(\d+)%$', None)
  assert processor._extract_progress('No match in dis string') == None

def test_eval_progress():
  # given a match in the string, should eval the result
  regex = r'(\d+)/(\d+)$'
  processor = ProcessController(regex, r'x[0] / x[1]')
  match = re.search(regex, '50/50')
  assert processor._eval_progress(match) == 1.0

def test_eval_progress_returns_none_on_failure():
  # given a match in the string, should eval the result
  regex = r'(\d+)/(\d+)$'
  processor = ProcessController(regex, r'x[0] *^/* x[1]')
  match = re.search(regex, '50/50')
  assert processor._eval_progress(match) == None
