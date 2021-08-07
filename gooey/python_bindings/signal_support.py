"""
Utilities for patching Windows so that CTRL-C signals
can be received by process groups.

The best resource for understanding why this is required is the Python
Issue here: https://bugs.python.org/issue13368

**The official docs from both Python and Microsoft cannot be trusted due to inaccuracies**

The two sources directly conflict with regards to what signals are possible on Windows
under which circumstances.


Python's docs:
    https://bugs.python.org/issue13368
    On Windows, SIGTERM is an alias for terminate(). CTRL_C_EVENT and
    CTRL_BREAK_EVENT can be sent to processes started with a creationflags
    parameter which includes CREATE_NEW_PROCESS_GROUP.

Microsoft's docs:
    https://docs.microsoft.com/en-us/windows/console/generateconsolectrlevent
    Generates a CTRL+C signal. This signal cannot be generated for process groups.

Another piece of the puzzle:
    https://docs.microsoft.com/en-us/windows/console/handlerroutine#remarks
    Each console process has its own list of HandlerRoutine functions. Initially,
    this list contains only a default handler function that calls ExitProcess. A
    console process adds or removes additional handler functions by calling the
    SetConsoleCtrlHandler function, which does not affect the list of handler
    functions for other processes.

The most important line here is: "Initially, this list contains only the default
handler function that calls exit Process"

So, despite what Microsoft's docs for ctrlcevent state, it IS possible to send
the ctrl+c signal to process groups **IFF** the leader for that process group has
the appropriate handler installed.

We can solve this transparently in Gooey land by installing the handler on behalf
of the user when required.
"""
import sys
import signal
from textwrap import dedent


def requires_special_handler(platform, requested_signal):
    """
    Checks whether we need to attach additional handlers
    to this process to deal with ctrl-C signals
    """
    return platform.startswith("win") and requested_signal == signal.CTRL_C_EVENT


def install_handler():
    """
    Adds a Ctrl+C 'handler routine'. This allows the CTRL-C
    signal to be received even when the process was created in
    a new process group.

    See module docstring for additional info.
    """
    assert sys.platform.startswith("win")
    import ctypes

    help_msg = dedent('''
    Please open an issue here: https://github.com/chriskiehl/Gooey/issues
        
    GOOD NEWS: THERE IS A WORK AROUND: 
    
    Gooey only needs to attach special Windows handlers for the CTRL-C event. Consider using 
    the `CTRL_BREAK_EVENT` or `SIGTERM` instead to get past this error. 
    
    See the Graceful Shutdown docs for information on how to catch alternative signals. 
    
    https://github.com/chriskiehl/Gooey/tree/master/docs 
    ''')

    try:
        kernel32 = ctypes.WinDLL('kernel32')
        if kernel32.SetConsoleCtrlHandler(None, 0) == 0:
            raise Exception(dedent('''
            Gooey was unable to install the handler required for processing
            CTRL-C signals. This is a **very** unexpected failure. 
            ''') + help_msg)
    except OSError as e:
        raise OSError(dedent('''
            Gooey failed while trying to find the kernel32 module. 
            Gooey requires this module in order to attach handlers for CTRL-C signal. 
            Not being able to find this is **very** unexpected. 
            ''') + help_msg)
