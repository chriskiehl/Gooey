import unittest
from argparse import ArgumentParser

from python_bindings import constants
from python_bindings.config_generator import create_from_parser
from gooey.tests import *
from gooey.python_bindings.parameters import gooey_params


class TextConfigGenerator(unittest.TestCase):

    def test_program_description(self):
        """
        Should use `program_description` if supplied, otherwise
        fallback to the description on the `parser`
        """

        parser = ArgumentParser(description="Parser Description")
        # when supplied explicitly, we assign it as the description
        params = gooey_params(program_description='Custom Description')
        buildspec = create_from_parser(parser, "", **params)
        self.assertEqual(buildspec['program_description'], 'Custom Description')

        # when no explicit program_definition supplied, we fallback to the parser's description
        buildspec = create_from_parser(parser, "", **gooey_params())
        self.assertEqual(buildspec['program_description'], 'Parser Description')

        # if no description is provided anywhere, we just set it to be an empty string.
        blank_parser = ArgumentParser()
        buildspec = create_from_parser(blank_parser, "", **gooey_params())
        self.assertEqual(buildspec['program_description'], '')

    def test_valid_font_weights(self):
        """
        Asserting that only valid font-weights are allowable.
        """
        all_valid_weights = range(100, 1001, 100)
        for weight in all_valid_weights:
            parser = ArgumentParser(description="test parser")
            params = gooey_params(terminal_font_weight=weight)
            buildspec = create_from_parser(parser, "", **params)
            self.assertEqual(buildspec['terminal_font_weight'], weight)

    def test_font_weight_defaults_to_normal(self):
        parser = ArgumentParser(description="test parser")
        # no font_weight explicitly provided
        buildspec = create_from_parser(parser, "", **gooey_params())
        self.assertEqual(buildspec['terminal_font_weight'], constants.FONTWEIGHT_NORMAL)


    def test_invalid_font_weights_throw_error(self):
        parser = ArgumentParser(description="test parser")
        with self.assertRaises(ValueError):
            invalid_weight = 9123
            params = gooey_params(terminal_font_weight=invalid_weight)
            buildspec = create_from_parser(parser, "", **params)


if __name__ == '__main__':
    unittest.main()
