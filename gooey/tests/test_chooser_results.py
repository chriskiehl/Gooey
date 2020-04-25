import argparse
import os
import unittest

from unittest.mock import patch
from gooey.gui.components.widgets.core import chooser

class TestChooserResults(unittest.TestCase):

    @patch('gooey.gui.components.widgets.core.chooser.MDD')
    def test_multiDirChooserGetResult(self, mockWxMDD):

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
            if osname and osname == os.name:
                mockWxMDD.GetPaths.return_value = pathsoutput
                result = chooser.MultiDirChooser.getResult(None, mockWxMDD)
                self.assertEqual(result, expected)
