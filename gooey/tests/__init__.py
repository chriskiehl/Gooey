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
import locale
import platform

class TestApp(wx.App):
    """
    Stolen from the mailing list here:
    https://groups.google.com/g/wxpython-users/c/q5DSyyuKluA

    Wx started randomly exploding with locale issues while running
    the tests. For whatever reason, manually setting it in InitLocale
    seems to solve the problem.
    """
    def __init__(self, with_c_locale=None, **kws):
        if with_c_locale is None:
            with_c_locale = (platform.system() == 'Windows')
        self.with_c_locale = with_c_locale
        wx.App.__init__(self, **kws)

    def InitLocale(self):
        """over-ride wxPython default initial locale"""
        if self.with_c_locale:
            self._initial_locale = None
            locale.setlocale(locale.LC_ALL, 'C')
        else:
            lang, enc = locale.getdefaultlocale()
            self._initial_locale = wx.Locale(lang, lang[:2], lang)
            locale.setlocale(locale.LC_ALL, lang)

    def OnInit(self):
        self.createApp()
        return True

    def createApp(self):
        return True


app = None

def setUpModule():
    global app
    app = TestApp()

def tearDownModule():
    global app
    app.Destroy()