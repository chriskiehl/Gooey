"""
This weirdness exists to work around a very specific problem
with testing WX: you can only ever have one App() instance per
process. I've spent hours and hours trying to work around this and
figure out how to gracefully destroy and recreate them, but... no dice.

This is echo'd in the docs: https://wxpython.org/Phoenix/docs/html/wx.App.html

Destroying/recreating causes instability in the tests. We can work around that
by reusing the same App instance across tests and only destroying the top level
frame (which is fine). However, this causes a new problem: the last test which
runs will now always fail, cause we're not Destroying the App instance.

Ideal world: UnitTest would expose a global "done" hook regardless of test
discovery type. That doesn't exist, so the best we can do is use the Module cleanup
methods. These aren't perfect, but destroying / recreating at the module boundary
gives slightly more reliable tests. These are picked up by the test runner
by their existence in the module's globals(). There's no other way to hook
things together. We need it in every test, and thus... that's the background
for why this weirdness is going on.

It's a hack around a hack around a problem in Wx.

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
    app = wx.App()

def tearDownModule():
    global app
    app.Destroy()