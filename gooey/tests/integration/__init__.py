"""
Integration tests that exercise Gooey's various run modes

WX Python needs to control the main thread. So, in order to simulate a user
running through the system, we have to execute the actual assertions in a
different thread
"""