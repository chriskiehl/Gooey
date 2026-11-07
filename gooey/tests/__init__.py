"""
This weirdness exists to work around a very specific problem
with testing WX: you can only ever have one App() instance per
process. Destroying and recreating it is unreliable, see
https://wxpython.org/Phoenix/docs/html/wx.App.html

Destroying the App between test modules crashes the process when the
tests are run with pytest. So instead, the first test module to run
creates the App and every later module reuses it. Only the top level
frame is destroyed between tests (see harness.instrumentGooey). The App
itself is cleaned up when the test process exits.

The App is created in setUpModule, which the test runner (unittest or
pytest) picks up by its existence in the test module's globals().

Usage:

In any tests which use WX, you must import this module's definitions
into the test's global scope

```
from gooey.tests import *
```
"""
import wx

app = None

def setUpModule():
    global app
    if app is None:
        app = wx.App()
