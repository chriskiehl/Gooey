import json
import unittest
from argparse import ArgumentParser
from typing import Dict
from unittest.mock import MagicMock, patch

from python_bindings.dynamics import patch_argument, check_value
from gooey.python_bindings import control
from gooey.python_bindings.parameters import gooey_params

# TODO:
# TODO:
# TODO:
# TODO:
# TODO:
class TestControl(unittest.TestCase):

    def test_validate_form(self):
        writer = MagicMock()
        exit = MagicMock()
        monkey_patch = control.validate_form(gooey_params(), write=writer, exit=exit)
        ArgumentParser.original_parse_args = ArgumentParser.parse_args
        ArgumentParser.parse_args = monkey_patch

        parser = ArgumentParser()
        parser.add_argument('foo', type=int)
        parser.add_argument('bar', type=float)
        parser.add_argument('baz', choices=[1, 2, 3])

        # 3 wrong answers should yield 3 validation errors
        # note that the last one is a choices validation, which exercises
        # the check_value code paths as well. See: test_dynamics.
        parser.parse_args(['not-an-int', 'not-a-float', 'wrong-choice'])
        # we should've 'written' to stdout and 'exited' under happy-path conditions
        assert writer.called
        assert exit.called

        # our 3 validation errors reported as json
        result = json.loads(writer.call_args[0][0])
        assert len(result) == 3
        assert 'foo' in result
        assert 'bar' in result
        assert 'baz' in result





