import os
import re
import subprocess
import sys
from functools import partial
from threading import Thread

from gooey.gui import events
from gooey.gui.pubsub import pub
from gooey.gui.util.casting import safe_float
from gooey.gui.util.taskkill import taskkill
from gooey.util.functional import unit, bind


class ProcessController(object):
    def __init__(self, progress_regex, progress_expr, hide_progress_msg,
                 encoding, shell=True):
        self._process = None
        self.progress_regex = progress_regex
        self.progress_expr = progress_expr
        self.hide_progress_msg = hide_progress_msg
        self.encoding = encoding
        self.wasForcefullyStopped = False
        self.shell_execution = shell

    def was_success(self):
        self._process.communicate()
        return self._process.returncode == 0

    def poll(self):
        if not self._process:
            raise Exception('Not started!')
        self._process.poll()

    def stop(self):
        if self.running():
            self.wasForcefullyStopped = True
            taskkill(self._process.pid)

    def running(self):
        return self._process and self.poll() is None

    def run(self, command):
        self.wasForcefullyStopped = False
        env = os.environ.copy()
        env["GOOEY"] = "1"
        env["PYTHONIOENCODING"] = self.encoding
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

    def format_interval(self,time_value):
        """
        Formats a number of seconds as a clock time, [H:]MM:SS
        Parameters
        ----------
        t  : int
            Number of seconds.
        Returns
        -------
        out  : str
            [H:]MM:SS
        """
        # https://github.com/tqdm/tqdm/blob/0cd9448b2bc08125e74538a2aea6af42ee1a7b6f/tqdm/std.py#L228
        mins, s = divmod(int(time_value), 60)
        h, m = divmod(mins, 60)
        if h:
            return '{0:d}:{1:02d}:{2:02d}'.format(h, m, s)
        else:
            return '{0:02d}:{1:02d}'.format(m, s)


    def _calculate_time_remaining(self,progress,start_time):
        # https://github.com/tqdm/tqdm/blob/0cd9448b2bc08125e74538a2aea6af42ee1a7b6f/tqdm/std.py#L392
        # https://github.com/tqdm/tqdm/blob/0cd9448b2bc08125e74538a2aea6af42ee1a7b6f/tqdm/std.py#L417
        _stop_time = self._get_current_time()
        _elapsed = _stop_time - start_time
        _rate = progress / _elapsed
        return _elapsed,((100 - progress) / _rate)

    def _get_current_time(self):
        try:
            from time import perf_counter
            return perf_counter()
        except:
            import timeit
            return timeit.default_timer()

    def _forward_stdout(self, process):
        '''
        Reads the stdout of `process` and forwards lines and progress
        to any interested subscribers
        '''
        _start_time = self._get_current_time()
        while True:
            line = process.stdout.readline()
            if not line:
                break
            _progress = self._extract_progress(line)
            if _progress > 0:
                _elapsed_time, _time_remaining = self._calculate_time_remaining(_progress,_start_time)
                _elapsed_str = self.format_interval(_elapsed_time)
                _remaining_str = self.format_interval(_time_remaining)
                pub.send_message(events.TIME_REMAINING_UPDATE,elapsed_time=_elapsed_str,time_remaining=_remaining_str)
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
