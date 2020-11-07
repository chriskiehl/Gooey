import argparse
import os
import unittest

from gooey.gui.components.widgets.core import chooser
from gooey.tests import *


class MockWxMDD:
    def GetPaths(self):
        pass

class TestChooserResults(unittest.TestCase):

    def test_multiDirChooserGetResult(self):
        expected_outputs = [
            (None, "", [""]),

            # Windows
            ('nt', "C:", ["OS and System (C:)"]),
            ('nt', "D:\\A Folder\\Yep Another One",
             ["Other Stuff (D:)\\A Folder\\Yep Another One"]),
            ('nt', "A:\\Wow Remember Floppy Drives;E:\\Righto Then",
             ["Flipflop (A:)\\Wow Remember Floppy Drives",
              "Elephants Only (E:)\\Righto Then"])
        ]

        for osname, expected, pathsoutput in expected_outputs:
            if not osname or osname == os.name:
                chooser.MDD.MultiDirDialog = MockWxMDD
                chooser.MDD.MultiDirDialog.GetPaths = lambda self : pathsoutput
                result = chooser.MultiDirChooser.getResult(None, MockWxMDD())
                print(result)
                self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
