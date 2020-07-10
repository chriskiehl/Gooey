"""
Module for evaluating time elapsed & time remaining from progress
"""
import wx
from gooey.gui.pubsub import pub
from gooey.gui import events

class Timing(object):

    def __init__(self, parent):
        self.startTime = 0
        self.estimatedRemaining = None
        self.wxTimer = wx.Timer(parent)
        self.parent = parent
        parent.Bind(wx.EVT_TIMER, self.publishTime, self.wxTimer)

        pub.subscribe(events.PROGRESS_UPDATE, self._updateEstimate)

    def _updateEstimate(self, *args, **kwargs):
        prog = kwargs.get('progress')
        if(not prog): 
            self.estimatedRemaining = None
            return
        if(prog > 0):
            self.estimatedRemaining = estimate_time_remaining(prog,self.startTime)

    def publishTime(self, *args, **kwargs):
        pub.send_message(
            events.TIME_UPDATE,
            start=self.startTime,
            current=get_current_time(),
            elapsed_time=format_interval(get_elapsed_time(self.startTime)),
            estimatedRemaining=format_interval(self.estimatedRemaining))

    def start(self):
        self.startTime = get_current_time()
        self.estimatedRemaining = None
        self.wxTimer.Start()

    def stop(self):
        self.wxTimer.Stop()

def format_interval(timeValue):
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
    try:
        mins, s = divmod(int(timeValue), 60)
        h, m = divmod(mins, 60)
        if h:
            return '{0:d}:{1:02d}:{2:02d}'.format(h, m, s)
        else:
            return '{0:02d}:{1:02d}'.format(m, s)
    except:
        return None

def get_elapsed_time(startTime):
    """
    Get elapsed time in form of seconds. Provide a start time in seconds as float.

    Args:
        startTime (float): Start time to compare against in seconds.

    Returns:
        float: Time between start time and now
    """
    return get_current_time() - startTime

def estimate_time_remaining(progress,startTime):
    # https://github.com/tqdm/tqdm/blob/0cd9448b2bc08125e74538a2aea6af42ee1a7b6f/tqdm/std.py#L392
    # https://github.com/tqdm/tqdm/blob/0cd9448b2bc08125e74538a2aea6af42ee1a7b6f/tqdm/std.py#L417
    _rate = progress / get_elapsed_time(startTime)
    return ((100 - progress) / _rate)

def get_current_time():
    """
    Returns a float of the current time in seconds. Attempt to import perf_counter (more accurate in 3.4+), otherwise utilise timeit.

    Returns:
        float: Current time in seconds from performance counter.
    """
    try:
        from time import perf_counter
        return perf_counter()
    except:
        import timeit
        return timeit.default_timer()
