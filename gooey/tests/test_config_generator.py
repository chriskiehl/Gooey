import unittest
from argparse import ArgumentParser

from python_bindings.config_generator import create_from_parser


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


if __name__ == '__main__':
    unittest.main()