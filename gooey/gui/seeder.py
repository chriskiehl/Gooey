"""
Util for talking to the client program in order to retrieve
dynamic defaults for the UI
"""
import subprocess
from json import JSONDecodeError
from subprocess import CalledProcessError

from gooey.python_bindings.types import Try, Success, Failure
from gooey.python_bindings.coms import deserialize_inbound


def communicate(cmd, encoding) -> Try:
    """
    Invoke the processes specified by `cmd`.
    Assumes that the process speaks JSON over stdout. Non-json response
    are treated as an error.

    Implementation Note: I don't know why, but `Popen` is like ~5-6x faster
    than `check_output`. in practice, it means waiting for ~1/10th
    of a second rather than ~7/10ths of a second. A
    difference which is pretty weighty when there's a
    user waiting on the other end.
    """
    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        out, err = proc.communicate()
        if out and proc.poll() == 0:
            return Success(deserialize_inbound(out, encoding))
        else:
            return Failure(CalledProcessError(proc.returncode, cmd, output=out, stderr=err))
    except JSONDecodeError as e:
        return Failure(e)

