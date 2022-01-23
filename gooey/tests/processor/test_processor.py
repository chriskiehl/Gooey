import re
import signal
import subprocess
import sys
import unittest
import os
import time

import wx

from gooey.gui import events, processor
from gooey.gui.pubsub import pub
from gooey.gui.processor import ProcessController


class TestProcessor(unittest.TestCase):

    def test_extract_progress(self):
        # should pull out a number based on the supplied
        # regex and expression
        processor = ProcessController(r"^progress: (\d+)%$", None, False, 'utf-8')
        self.assertEqual(processor._extract_progress(b'progress: 50%'), 50)

        processor = ProcessController(r"total: (\d+)%$", None, False, 'utf-8')
        self.assertEqual(processor._extract_progress(b'my cool total: 100%'), 100)

    def test_extract_progress_returns_none_if_no_regex_supplied(self):
        processor = ProcessController(None, None, False, 'utf-8')
        self.assertIsNone(processor._extract_progress(b'Total progress: 100%'))


    def test_extract_progress_returns_none_if_no_match_found(self):
        processor = ProcessController(r'(\d+)%$', None, False, 'utf-8')
        self.assertIsNone(processor._extract_progress(b'No match in dis string'))


    def test_eval_progress(self):
        # given a match in the string, should eval the result
        regex = r'(\d+)/(\d+)$'
        processor = ProcessController(regex, r'x[0] / x[1]', False,False, 'utf-8')
        match = re.search(regex, '50/50')
        self.assertEqual(processor._eval_progress(match), 1.0)
    def test_eval_progress_returns_none_on_failure(self):
        # given a match in the string, should eval the result
        regex = r'(\d+)/(\d+)$'
        processor = ProcessController(regex, r'x[0] *^/* x[1]', False, False,'utf-8')
        match = re.search(regex, '50/50')
        self.assertIsNone(processor._eval_progress(match))


    def test_all_interrupts_halt_process(self):
        """
        TODO: These tests are hella flaky. I'm confident that the feature works. However, getting
        signals, subprocesses and unittest to all play together reliably is proving tricky. It
        primarily seems to come down to how long the time.sleep() is before sending the shutdown
        signal.
        """

        cmd = 'python ' + os.path.join(os.getcwd(), 'files', 'infinite_loop.py')

        try:
            import _winapi
            signals = [signal.SIGTERM, signal.CTRL_BREAK_EVENT, signal.CTRL_C_EVENT]
        except ModuleNotFoundError:
            signals = [signal.SIGTERM, signal.SIGINT]
        try:
            for sig in signals:
                print('sig', sig)
                processor = ProcessController(None, None, False, 'utf-8', True, shutdown_signal=sig)

                processor.run(cmd)
                self.assertTrue(processor.running())

                # super-duper important sleep so that the
                # signal is actually received by the child process
                # see: https://stackoverflow.com/questions/32023719/how-to-simulate-a-terminal-ctrl-c-event-from-a-unittest
                time.sleep(1)
                processor.stop()
                max_wait = time.time() + 4
                while processor.running() and time.time() < max_wait:
                    time.sleep(0.1)
                self.assertFalse(processor.running())
        except KeyboardInterrupt:
            pass


    def test_ignore_sigint_family_signals(self):
        try:
            import _winapi
            signals = [signal.CTRL_BREAK_EVENT, signal.CTRL_C_EVENT]
            programs = ['ignore_break.py', 'ignore_interrupt.py']
        except ModuleNotFoundError:
            signals = [signal.SIGINT]
            programs = ['ignore_interrupt.py']


        for program, sig in zip(programs, signals):
            cmd = sys.executable + ' ' + os.path.join(os.getcwd(), 'files', program)
            process = processor = ProcessController(None, None, False, 'utf-8', True, shutdown_signal=sig, testmode=True)
            process.run(cmd)
            # super-duper important sleep so that the
            # signal is actually received by the child process
            # see: https://stackoverflow.com/questions/32023719/how-to-simulate-a-terminal-ctrl-c-event-from-a-unittest
            time.sleep(1)
            process.send_shutdown_signal()
            # wait to give stdout enough time to write
            time.sleep(1)
            # now our signal should have been received, but rejected.
            self.assertTrue(processor.running())
            # so we sigterm to actually shut down the process.
            process._send_signal(signal.SIGTERM)
            # sanity wait
            max_wait = time.time() + 2
            while processor.running() and time.time() < max_wait:
                time.sleep(0.1)
            # now we should be shut down due to killing the process.
            self.assertFalse(processor.running())
            # and we'll see in the stdout out from the process that our
            # interrupt was received
            output = process._process.stdout.read().decode('utf-8')
            self.assertIn("INTERRUPT", str(output))
            # but indeed ignored. It continued running and writing to stdout after
            # receiving the signal
            self.assertTrue(output.index("INTERRUPT") < len(output))

