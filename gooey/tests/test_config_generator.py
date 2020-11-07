import unittest
from argparse import ArgumentParser

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


if __name__ == '__main__':
    unittest.main()