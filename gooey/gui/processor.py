import signal
from contextlib import contextmanager
import signal
import psutil
import wx
import os
import re
import subprocess
import sys
from functools import partial
from threading import Thread

from gooey.gui import events
from gooey.gui.pubsub import pub
from gooey.gui.util.casting import safe_float
from gooey.util.functional import unit, bind


class ProcessController(object):
    def __init__(self, progress_regex, progress_expr, hide_progress_msg,
                 encoding, shell=True, shutdown_signal=signal.SIGTERM):
        self._process = None
        self.progress_regex = progress_regex
        self.progress_expr = progress_expr
        self.hide_progress_msg = hide_progress_msg
        self.encoding = encoding
        self.wasForcefullyStopped = False
        self.shell_execution = shell
        self.shutdown_signal = shutdown_signal

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

        Note on the bizarre Thread spawning. For some reason, it seems to be
        required in order to get the signal we're sending to actually get
        pushed to the child process. Why that is, I have **absolutely no idea**.
        I've no idea why it needs to be jiggled or why it works. It was just stumbled
        upon experimentally after noticing that the child process would only
        respond to the signal after clicking the stop button again.
        This is all just to say... it's magic and needs to be there.
        Possible due to:
        stackoverflow.com/questions/32023719/how-to-simulate-a-terminal-ctrl-c-event-from-a-unittest
        """
        with ignore_signal():
            if self.running():
                self.wasForcefullyStopped = True
                self.send_shutdown_signal()

                # for some reason, this is required, even though
                # it literally does nothing(???). See Docstring for
                # additional details.
                Thread(target=lambda: None).start()


    def send_shutdown_signal(self):
        parent = psutil.Process(self._process.pid)
        for child in parent.children(recursive=True):
            print(child)
            child.send_signal(self.shutdown_signal)
        parent.send_signal(self.shutdown_signal)


    def running(self):
        return self._process and self.poll() is None

    def run(self, command):
        self.wasForcefullyStopped = False
        env = os.environ.copy()
        env["GOOEY"] = "1"
        env["PYTHONIOENCODING"] = self.encoding
        # TODO: why is this try/catch here..?
        try:
            self._process = subprocess.Popen(
                command.encode(sys.getfilesystemencoding()),
                stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                stderr=subprocess.STDOUT, shell=self.shell_execution, env=env)
        except:
            self._process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                stderr = subprocess.STDOUT, shell = self.shell_execution, env=env)

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

@contextmanager
def ignore_signal():
    """
    Ignores incoming ctrl_break signals for the duration
    of this context. Default behavior is returned upon completion.

    When we create a subprocess on Windows, the new process gets
    rolled into the current process' Process Group. Signals get sent
    to all members of a process group[0], which means that the Gooey
    process would end up receiving the BREAK signal that it itself is
    sending to its child process. So while gooey is sending signals
    we ignore any incoming so that we don't inadvertently shut ourselves
    down.

    [0] There actually seems to be some kind of bubbling of signals going
    on that I don't fully understand. IF the child process attaches a BREAK
    signal handler, than the parent process does NOT see the signal. It's only
    when the child process doesn't respond that Gooey sees it as well.
    """
    signal.signal(signal.SIGBREAK, signal.SIG_IGN)
    try:
        yield
    except KeyboardInterrupt:
        # similar to the BREAK signal, the KeyboardInterrupt can
        # fire here as well. Silently ignoring is the Right Thing.
        pass
    finally:
        signal.signal(signal.SIGBREAK, signal.SIG_DFL)
