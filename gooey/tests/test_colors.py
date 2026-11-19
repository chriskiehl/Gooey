import unittest
from unittest.mock import MagicMock, patch

from gooey.python_bindings import colors


class TestColors(unittest.TestCase):

    def test_is_dark_mode(self):
        # Gooey uses dark colors when the system draws windows with a dark
        # background. wx can only check this once a wx.App exists, and on
        # Linux (GTK) it crashes instead of raising an error if there is none.
        testcases = [
            # C1: A wx.App exists and windows have a dark background.
            # Expected: Dark mode is on.
            (True, True, True),
            # C2: A wx.App exists and windows have a light background.
            # Expected: Dark mode is off.
            (True, False, False),
            # C3: No wx.App exists, even though the system is dark.
            # Expected: Dark mode is off and the system appearance is not
            # checked, so wx cannot crash.
            (False, True, False),
        ]
        for input_app_exists, input_dark_background, expected_dark_mode in testcases:
            with self.subTest(app_exists=input_app_exists, dark_background=input_dark_background):
                system_settings = MagicMock()
                system_settings.GetAppearance.return_value.IsUsingDarkBackground.return_value = input_dark_background
                running_app = MagicMock() if input_app_exists else None
                with patch('wx.GetApp', return_value=running_app), patch('wx.SystemSettings', system_settings):
                    actual_dark_mode = colors.is_dark_mode()
                    actual_appearance_checked = system_settings.GetAppearance.called
                self.assertEqual(actual_dark_mode, expected_dark_mode)
                self.assertEqual(actual_appearance_checked, input_app_exists)


if __name__ == '__main__':
    unittest.main()
