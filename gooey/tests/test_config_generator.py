import unittest
from argparse import ArgumentParser
from unittest.mock import patch

from gooey import GooeyParser
from python_bindings import constants
from python_bindings.config_generator import create_from_parser
from gooey.tests import *

class TextConfigGenerator(unittest.TestCase):

    def test_program_description(self):
        """
        Should use `program_description` if supplied, otherwise
        fallback to the description on the `parser`
        """

        parser = ArgumentParser(description="Parser Description")
        # when supplied explicitly, we assign it as the description
        buildspec = create_from_parser(parser, "", program_description='Custom Description')
        self.assertEqual(buildspec['program_description'], 'Custom Description')

        # when no explicit program_definition supplied, we fallback to the parser's description
        buildspec = create_from_parser(parser, "")
        self.assertEqual(buildspec['program_description'], 'Parser Description')

        # if no description is provided anywhere, we just set it to be an empty string.
        blank_parser = ArgumentParser()
        buildspec = create_from_parser(blank_parser, "")
        self.assertEqual(buildspec['program_description'], '')

    def test_valid_font_weights(self):
        """
        Asserting that only valid font-weights are allowable.
        """
        all_valid_weights = range(100, 1001, 100)
        for weight in all_valid_weights:
            parser = ArgumentParser(description="test parser")
            buildspec = create_from_parser(parser, "", terminal_font_weight=weight)
            self.assertEqual(buildspec['terminal_font_weight'], weight)

    def test_font_weight_defaults_to_normal(self):
        parser = ArgumentParser(description="test parser")
        # no font_weight explicitly provided
        buildspec = create_from_parser(parser, "")
        self.assertEqual(buildspec['terminal_font_weight'], constants.FONTWEIGHT_NORMAL)


    def test_invalid_font_weights_throw_error(self):
        parser = ArgumentParser(description="test parser")
        with self.assertRaises(ValueError):
            invalid_weight = 9123
            buildspec = create_from_parser(parser, "", terminal_font_weight=invalid_weight)


    def test_default_colors_follow_system_appearance(self):
        # Gooey picks its default colors to match the system appearance, so
        # text stays readable in dark mode. Colors the user sets are always
        # kept. Each case builds a program with one group and one widget,
        # then reads back the window, group, and widget colors.
        light_colors = {
            'body_bg_color': '#f0f0f0',
            'header_bg_color': '#ffffff',
            'footer_bg_color': '#f0f0f0',
            'sidebar_bg_color': '#f2f2f2',
            'terminal_panel_color': '#F0F0F0',
            'terminal_font_color': '#000000',
            'group_label_color': '#000000',
            'group_description_color': '#363636',
            'widget_label_color': '#000000',
            'widget_help_color': '#363636',
        }
        dark_colors = {
            'body_bg_color': '#292A31',
            'header_bg_color': '#19191D',
            'footer_bg_color': '#292A31',
            'sidebar_bg_color': '#292A31',
            'terminal_panel_color': '#3A3A44',
            'terminal_font_color': '#ffffff',
            'group_label_color': '#ffffff',
            'group_description_color': '#E1E1E3',
            'widget_label_color': '#ffffff',
            'widget_help_color': '#EDEDF0',
        }
        testcases = [
            # C1: Light mode and no colors set by the user.
            # Expected: The light colors Gooey has always used.
            (False, {}, {}, light_colors),
            # C2: Dark mode and no colors set by the user.
            # Expected: The dark colors.
            (True, {}, {}, dark_colors),
            # C3: Dark mode with a window color and a widget color set by the user.
            # Expected: The user's colors are kept and the rest are dark.
            (True, {'body_bg_color': '#123456'}, {'label_color': '#abcdef'},
             dict(dark_colors, body_bg_color='#123456', widget_label_color='#abcdef')),
        ]
        for input_dark_mode, input_options, input_widget_options, expected_colors in testcases:
            with self.subTest(dark_mode=input_dark_mode, options=input_options, widget_options=input_widget_options):
                parser = GooeyParser()
                group = parser.add_argument_group('Group name', 'Group description')
                group.add_argument('--foo', help='Foo help', gooey_options=input_widget_options)
                with patch('gooey.python_bindings.colors.is_dark_mode', return_value=input_dark_mode):
                    buildspec = create_from_parser(parser, '', **input_options)
                group_spec = list(buildspec['widgets'].values())[0]['contents'][0]
                widget_options = group_spec['items'][0]['options']
                actual_colors = {
                    'body_bg_color': buildspec['body_bg_color'],
                    'header_bg_color': buildspec['header_bg_color'],
                    'footer_bg_color': buildspec['footer_bg_color'],
                    'sidebar_bg_color': buildspec['sidebar_bg_color'],
                    'terminal_panel_color': buildspec['terminal_panel_color'],
                    'terminal_font_color': buildspec['terminal_font_color'],
                    'group_label_color': group_spec['options']['label_color'],
                    'group_description_color': group_spec['options']['description_color'],
                    'widget_label_color': widget_options['label_color'],
                    'widget_help_color': widget_options['help_color'],
                }
                self.assertEqual(actual_colors, expected_colors)


if __name__ == '__main__':
    unittest.main()