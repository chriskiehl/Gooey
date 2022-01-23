import os
import re
import signal
import subprocess
import sys
from functools import partial
from threading import Thread

import psutil  # type: ignore

from gooey.gui import events
from gooey.gui.pubsub import pub
from gooey.gui.util.casting import safe_float
from gooey.util.functional import unit, bind
from gooey.python_bindings.types import GooeyParams


try:
    import _winapi
    creationflag = subprocess.CREATE_NEW_PROCESS_GROUP
except ModuleNotFoundError:
    # default Popen creation flag
    creationflag = 0


class ProcessController(object):

    @classmethod
    def of(cls, params: GooeyParams):
        return cls(
            params.get('progress_regex'),
            params.get('progress_expr'),
            params.get('hide_progress_msg'),
            params.get('encoding'),
            params.get('requires_shell'),
            params.get('shutdown_signal', signal.SIGTERM)
        )

    def __init__(self, progress_regex, progress_expr, hide_progress_msg,
                 encoding, shell=True, shutdown_signal=signal.SIGTERM, testmode=False):
        self._process = None
        self.progress_regex = progress_regex
        self.progress_expr = progress_expr
        self.hide_progress_msg = hide_progress_msg
        self.encoding = encoding
        self.wasForcefullyStopped = False
        self.shell_execution = shell
        self.shutdown_signal = shutdown_signal
        self.testMode = testmode

    def was_success(self):
        self._process.communicate()
        return self._process.returncode == 0

    def poll(self):
        if not self._process:
            raise Exception('Not started!')
        return self._process.poll()

    def stop(self):
        """
        Sends a signal of the user's choosing (default SIGTERM) to
        the child process.
        """
        if self.running():
            self.wasForcefullyStopped = True
            self.send_shutdown_signal()

    def send_shutdown_signal(self):
        self._send_signal(self.shutdown_signal)

    def _send_signal(self, sig):
        parent = psutil.Process(self._process.pid)
        for child in parent.children(recursive=True):
            child.send_signal(sig)
        parent.send_signal(sig)

    def running(self):
        return self._process and self.poll() is None

    def run(self, command):
        """
        Kicks off the user's code in a subprocess.

        Implementation Note: CREATE_NEW_SUBPROCESS is required to have signals behave sanely
        on windows. See the signal_support module for full background.
        """
        self.wasForcefullyStopped = False
        env = os.environ.copy()
        env["GOOEY"] = "1"
        env["PYTHONIOENCODING"] = self.encoding
        # TODO: why is this try/catch here..?
        try:
            self._process = subprocess.Popen(
                command.encode(sys.getfilesystemencoding()),
                stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                stderr=subprocess.STDOUT, shell=self.shell_execution, env=env,
                creationflags=creationflag)
        except:
            self._process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                stderr = subprocess.STDOUT, shell = self.shell_execution, env=env,
                creationflags=creationflag
            )

        # the message pump depends on the wx instance being initiated and its
        # mainloop running (to dispatch pubsub messages). This makes testing difficult
        # so we only spin up the thread when we're not testing.
        if not self.testMode:
            t = Thread(target=self._forward_stdout, args=(self._process,))
            t.start()

    def _forward_stdout(self, process):
        '''
        Reads the stdout of `process` and forwards lines and progress
        to any interested subscribers
        '''
        while True:
            line = process.stdout.readline()
            if not line:
                break
            _progress = self._extract_progress(line)

            pub.send_message(events.PROGRESS_UPDATE, progress=_progress)
            if _progress is None or self.hide_progress_msg is False:
                pub.send_message(events.CONSOLE_UPDATE,
                                 msg=line.decode(self.encoding))
        pub.send_message(events.EXECUTION_COMPLETE)

    def _extract_progress(self, text):
        '''
        Finds progress information in the text using the
        user-supplied regex and calculation instructions
        '''
        # monad-ish dispatch to avoid the if/else soup
        find = partial(re.search, string=text.strip().decode(self.encoding))
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

